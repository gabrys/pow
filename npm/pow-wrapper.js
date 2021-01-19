#!/usr/bin/env node

const child_process = require('child_process');
const fs = require('fs');
const path = require('path');


function main() {
  const pow_args = process.argv.slice(2);
  const script_dir = path.dirname(fs.realpathSync(process.argv[1]));
  const package_dir = path.dirname(script_dir);

  let cmd;

  if (process.platform === 'win32') {
    // this works when installed with npm install -g https://github.com/gabrys/pow.git
    cmd = path.join(package_dir, 'windows', 'pow.dist' , 'pow.exe');
  } else {
    // this works when installed yarn global add https://github.com/gabrys/pow.git
    cmd = path.join(package_dir, 'src', 'pow.py');
  }

  cp = child_process.spawnSync(cmd, pow_args, {stdio: 'inherit'});
  if (cp.error) {
    return 127;
  }
  return cp.status;
}


main();
