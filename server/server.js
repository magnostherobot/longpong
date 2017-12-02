#!/bin/node

const net = require('net');
const port = parseInt(process.argv[2]);

let running = false;
let clients = new Set();

function forward(d) {
  switch (d.command) {
    case 'start':
      if (!running) {
        running = true;
        console.log('game starting!');
        let t = [...clients]
          .map(x => x.scr_w)
          .reduce((a, b) => { return parseFloat(a) + parseFloat(b) }, 0);
        let i = 0;
        let time = (new Date()).getTime();
        [...clients]
          .sort((a, b) => { return a.scr_i - b.scr_i })
          .forEach((x) => {
            console.log('.');
            let m = {
              command: 'start',
              info: {
                total_w: t,
                offset: i
              },
              ball_id: 1,
              vel:  { x: 1,     y: 1 },
              pos:  { x: t / 2, y: 0.5 },
              size: { x: 0.05,  y: 0.05 },
              time: time
            };
            x.write(JSON.stringify(m));
            i += x.scr_w;
        });
      }
      break;
    case 'stop':
      if (!running) break;
      running = false;
      clients.clear();
    default:
      if (!d.time) d.time = (new Date()).getTime();
      clients.forEach(x => x.write(JSON.stringify(d)));
  }
}

function update(n, i) {
  if (i.scr_w) n.scr_w = i.scr_w;
  if (i.scr_i) n.scr_i = i.scr_i;
  clients.add(n);
}

let server = net.createServer((s) => {
  console.log('new client: ' + s.remoteAddress);
  
  s.on('data', (data) => {
    var d = JSON.parse(data.toString());
    console.log(d);

    console.log(d.info);
    console.log(d);
    if (d.command) {
      forward(d);
    } else if (d.info && !running) {
      update(s, d.info);
    } else {
      console.log('not expecting ' + JSON.stringify(d));
    }
  });
});

server.listen(port);

console.log('server started', port);
