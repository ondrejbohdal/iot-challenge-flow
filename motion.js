'use strict';

var ttn = require('ttn');

var region = 'toast.is.ed.ac.uk';
var appId = 'team_banff';

var client = new ttn.Client(region, appId, accessKey);
var total_motions = 0;

client.on('connect', function (connack) {
  console.log('[DEBUG]', 'Connect:', connack);
});

client.on('error', function (err) {
  console.error('[ERROR]', err.message);
});

client.on('activation', function (deviceId, data) {
  console.log('[INFO] ', 'Activation:', deviceId, JSON.stringify(data, null, 2));
});

client.on('device', null, 'down/scheduled', function (deviceId, data) {
  console.log('[INFO] ', 'Scheduled:', deviceId, JSON.stringify(data, null, 2));
});

client.on('message', function (deviceId, data) {
  var code = data.payload_raw.readUInt32LE(0);
  var dt = data.payload_raw.readUInt32LE(4);
  var count = data.payload_raw.readUInt32LE(8);
  if (code === 0xDEADC0DE) {
      var secs = dt / 1000;
      console.log("Detected", count, "motions during", secs, "seconds.");
      //console.info('[INFO] ', 'Message:', deviceId, JSON.stringify(data, null, 2));
      total_motions += count;
      console.log("Total number of detected motions is", total_motions);
  }
});

client.on('message', null, 'led', function (deviceId, led) {

  // Toggle the LED
  var payload = {
    led: !led
  };

  // If you don't have an encoder payload function:
  // var payload = [led ? 0 : 1];

  console.log('[DEBUG]', 'Sending:', JSON.stringify(payload));
  client.send(deviceId, payload);
});
