document.addEventListener("DOMContentLoaded", async () => {
  const isSynced = sessionStorage.getItem("moodle_synced") === "true";

  if (!isSynced) {
    try {
      console.log("Starting fetch...");
        sessionStorage.setItem("moodle_synced", "true");


      const response = await fetch(`${APP.CONFIG.BACKEND_API_URL}/sync_assignments`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include"
      });

      console.log("Response received:", response.status);

    //   if (response.ok) {
    //     sessionStorage.setItem("moodle_synced", "true");
    //   }

    } catch (err) {
      console.error("Sync error:", err);
    }
  }
});