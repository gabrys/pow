#!/usr/bin/env node

const child_process = require('child_process');
const fs = require('fs');
const path = require('path');


function main() {
  const script_dir = path.dirname(fs.realpathSync(process.argv[1]));
  const package_dir = path.dirname(script_dir);
  const pow_args = process.argv.slice(2);

  let cmd;

  if (process.platform === 'win32') {
    cmd = path.join(package_dir, 'windows', 'pow-runner.dist', 'pow-runner.exe');
  } else if (process.platform === 'linux') {
    cmd = path.join(package_dir, 'linux', 'pow-runner');
  } else if (process.platform === 'darwin') {
    cmd = path.join(package_dir, 'macos', 'pow-runner');
  } else {
    // Bring your own Python
    cmd = 'python3';
  }

  pow_args.unshift(path.join(package_dir, 'src', 'pow.py'));
  cp = child_process.spawnSync(cmd, pow_args, {stdio: 'inherit'});
  if (cp.error) {
    return 127;
  }
  return cp.status;
}


process.exit(main());
