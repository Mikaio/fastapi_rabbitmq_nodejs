module.exports = {
  apps: [{
    script: "main.js",
    instances: "max",
    exec_mode: "cluster"
  }]
}
