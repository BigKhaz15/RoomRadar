"""Disposable local architecture spike; Python standard library only."""
import concurrent.futures as cf
import json, math, platform, sqlite3, statistics, tempfile, threading, time
import urllib.request, urllib.error
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def status(report, now):
    if report is None:
        return {'label': 'Unknown', 'timestamp': None}
    return {'label': 'Unknown' if now-report['timestamp'] >= 3600 else 'Reported '+report['observation'], 'timestamp': report['timestamp']}


def main():
    with tempfile.TemporaryDirectory() as folder:
        db = str(Path(folder)/'reports.sqlite')
        with sqlite3.connect(db) as c:
            c.executescript('CREATE TABLE rooms(id TEXT PRIMARY KEY); INSERT INTO rooms VALUES ("TEST-101"); CREATE TABLE reports(acceptance_order INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT NOT NULL REFERENCES rooms(id), observation TEXT NOT NULL CHECK(observation IN ("Empty","Occupied")), timestamp REAL NOT NULL);')
        def accept(payload, fail=False, fixed_time=None):
            if set(payload) != {'roomIdentifier','observation'} or payload['observation'] not in ('Empty','Occupied'):
                raise ValueError('Invalid report fields or observation')
            with sqlite3.connect(db, timeout=10) as c:
                c.execute('PRAGMA foreign_keys=ON')
                # SQLite serializes all writes in this surrogate, not only a room.
                c.execute('BEGIN IMMEDIATE')
                if not c.execute('SELECT 1 FROM rooms WHERE id=?',(payload['roomIdentifier'],)).fetchone():
                    raise ValueError('Unknown room')
                timestamp = time.time() if fixed_time is None else fixed_time
                cur=c.execute('INSERT INTO reports(room,observation,timestamp) VALUES (?,?,?)',(payload['roomIdentifier'],payload['observation'],timestamp))
                report={'acceptanceOrder':cur.lastrowid,'roomIdentifier':payload['roomIdentifier'],'observation':payload['observation'],'timestamp':timestamp}
                if fail:
                    raise sqlite3.OperationalError('Injected failure before commit')
                c.commit()
                return report
        def rows():
            with sqlite3.connect(db) as c:
                return c.execute('SELECT acceptance_order, room, observation, timestamp FROM reports ORDER BY acceptance_order').fetchall()
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args): pass
            def do_POST(self):
                try:
                    if self.path != '/api/reports':
                        self.send_error(404); return
                    payload=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                    result=accept(payload); code=201
                except (ValueError,TypeError,KeyError):
                    result={'error':'Invalid report'}; code=400
                except sqlite3.Error:
                    result={'error':'Storage failed'}; code=500
                body=json.dumps(result).encode()
                self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
        class Server(ThreadingHTTPServer):
            request_queue_size=128
        server=Server(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
        url=f'http://127.0.0.1:{server.server_port}/api/reports'
        def post(payload):
            request=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
            with urllib.request.urlopen(request,timeout=10) as response:
                return response.status,json.load(response)
        def worker(i):
            payload={'roomIdentifier':'TEST-101','observation':'Empty' if i%2==0 else 'Occupied'}
            start=time.perf_counter()
            try:
                code,report=post(payload)
                return {'request':i,'http':code,'report':report,'latency_ms':(time.perf_counter()-start)*1000,'ok':code==201}
            except Exception as e:
                return {'request':i,'ok':False,'latency_ms':(time.perf_counter()-start)*1000,'error':str(e)}
        try:
            with cf.ThreadPoolExecutor(max_workers=10) as pool:
                results=list(pool.map(worker,range(100)))
            persisted=rows()
            verified=sum(r['ok'] and any(tuple([r['report']['acceptanceOrder'],r['report']['roomIdentifier'],r['report']['observation'],r['report']['timestamp']])==row for row in persisted) for r in results)
            checks={}
            checks['100 acknowledged reports match persisted rows']=verified==100 and len(persisted)==100
            checks['100 unique increasing acceptance orders']=len({r[0] for r in persisted})==100 and all(a[0]<b[0] for a,b in zip(persisted,persisted[1:]))
            before=rows()
            try:
                accept({'roomIdentifier':'TEST-101','observation':'Occupied'},fail=True)
                checks['failed write rolls back without accepting report']=False
            except sqlite3.OperationalError:
                checks['failed write rolls back without accepting report']=rows()==before
            rejected=0
            for payload in [{'roomIdentifier':'TEST-101','observation':'Empty','student_id':'x'}, {'roomIdentifier':'MISSING','observation':'Empty'}, {'roomIdentifier':'TEST-101','observation':'Invalid'}]:
                try: post(payload)
                except urllib.error.HTTPError as e: rejected+=e.code==400
            checks['three invalid submissions rejected without new rows']=rejected==3 and rows()==before
            a=accept({'roomIdentifier':'TEST-101','observation':'Empty'},fixed_time=10000)
            b=accept({'roomIdentifier':'TEST-101','observation':'Occupied'},fixed_time=10000)
            checks['equal timestamps resolved by acceptance order']=a['timestamp']==b['timestamp'] and a['acceptanceOrder']<b['acceptanceOrder'] and rows()[-1][0]==b['acceptanceOrder']
            report={'timestamp':10000,'observation':'Occupied'}
            checks['3599 seconds remains reported']=status(report,13599)['label']=='Reported Occupied'
            checks['3600 seconds becomes Unknown and retains timestamp']=status(report,13600)=={'label':'Unknown','timestamp':10000}
            checks['missing report becomes Unknown']=status(None,13600)=={'label':'Unknown','timestamp':None}
            latencies=sorted(r['latency_ms'] for r in results)
            output={'run_utc':datetime.now(timezone.utc).isoformat(),'environment':{'python':platform.python_version(),'sqlite':sqlite3.sqlite_version,'platform':platform.platform()},'method':'100 HTTP requests through ten worker threads to a local server; SQLite disposable surrogate; no browser or PostgreSQL','total_requests':100,'workers':10,'persisted_and_verified':verified,'http_successes':sum(r['ok'] for r in results),'http_successes_within_3s':sum(r['ok'] and r['latency_ms']<=3000 for r in results),'average_http_ms':round(statistics.mean(latencies),3),'p95_http_ms':round(latencies[math.ceil(.95*len(latencies))-1],3),'checks':checks,'all_checks_passed':all(checks.values()),'qas01_verified':False,'limitations':['No browser rendering or visible confirmation measured','No PostgreSQL transaction or deployed hosting validation','SQLite serializes all writes, whereas planned design coordinates acceptance per room','Expiration tested with supplied times, not live browser timers'],'requests':results}
            Path('results.json').write_text(json.dumps(output,indent=2)+'\n')
            print(json.dumps({k:v for k,v in output.items() if k!='requests'},indent=2))
            if not all(checks.values()):raise SystemExit(1)
        finally:
            server.shutdown();server.server_close();thread.join()

if __name__=='__main__':main()
