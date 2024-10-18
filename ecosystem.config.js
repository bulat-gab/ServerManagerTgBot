const isWindows = process.platform === "win32";

module.exports = {
  apps: [
    {
      name: "server_bot",
      script: "main.py",
      interpreter: isWindows ? "venv\\Scripts\\pythonw.exe" : "venv/bin/python",
      cwd: __dirname,
      watch: true,
      watch_options: {
        // Optional: Customize the watch options
        followSymlinks: false, // Follow symlinks
        usePolling: true, // Use polling for file changes
        interval: 1000, // Polling interval (in ms)
      },
      ignore_watch: ["deploy", "\\.git", "*.log"],
    },
  ],
};
