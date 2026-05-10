document.addEventListener("DOMContentLoaded", async () => {
    const btnLogin = document.getElementById("auth-btn-login");
    const emailInput = document.getElementById("login-email");
    const passwordInput = document.getElementById("login-password");
    const errorEl = document.getElementById('login-error');

    // ── 1. Init LIFF (ดึง LIFF_ID จาก Backend) ───────────────
    try {
        const cfg = await fetch(`${APP.CONFIG.BACKEND_API_URL}/api/app-config`)
            .then(r => r.json());
        await liff.init({ liffId: cfg.liff_id });
    } catch (err) {
        console.error("LIFF init failed:", err);
    }

    // ── 2. ดึง LINE Profile (ถ้า login LINE แล้ว) ──────────────
    let lineProfile = null;
    if (liff.isLoggedIn()) {
        try {
            lineProfile = await liff.getProfile();
            // lineProfile = { userId, displayName, pictureUrl }
            console.log("LINE Profile:", lineProfile);
        } catch (err) {
            console.error("getProfile failed:", err);
        }
    } else {
        // ถ้ายังไม่ได้ login LINE ให้ redirect ไป LINE Login
        // (เฉพาะเมื่อเปิดใน LIFF Browser)
        if (liff.isInClient()) {
            liff.login({ redirectUri: APP.CONFIG.LIFF_REDIRECT_URL });
            return;
        }
    }

    // ── 3. Login ปกติ ──────────────────────────────────────────
    btnLogin.addEventListener("click", async () => {
        const username = emailInput.value.trim();
        const password = passwordInput.value;

        if (!username || !password) {
            errorEl.textContent = 'กรุณากรอกข้อมูลให้ครบถ้วน';
            errorEl.style.display = 'block';
            return;
        }

        btnLogin.disabled = true;
        btnLogin.textContent = "กำลังตรวจสอบ...";
        errorEl.style.display = 'none';

        try {
            const response = await fetch(`${APP.CONFIG.BACKEND_API_URL}/api/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    username,
                    password,
                    // ส่ง LINE userId ไปพร้อมกันเลย (ถ้ามี)
                    line_user_id: lineProfile?.userId ?? null,
                    line_display_name: lineProfile?.displayName ?? null,
                }),
                credentials: "include"
            });

            const data = await response.json();

            if (response.ok) {
                sessionStorage.setItem("token", data.token)
                const taskRes = await fetch(`${APP.CONFIG.BACKEND_API_URL}/api/tasks`, {
                    method: "GET",
                    headers: { "Content-Type": "application/json" ,
                               "Authorization": `Bearer ${data.token}`
                    },
                 
                });

                const taskJson = await taskRes.json();
                sessionStorage.setItem("tasks_cache", JSON.stringify(taskJson.data));

                if(data.is_new_user == false) sessionStorage.setItem("moodle_synced", "false");
                else sessionStorage.setItem("moodle_synced", "true");

                sessionStorage.setItem('isLoggedIn', 'true');
                sessionStorage.setItem("user", JSON.stringify({
                    username: data.username,
                    display_name: data.display_name,
                    line_user_id: lineProfile?.userId ?? null,
                }));

                window.location.replace("student.html");
            } else {
                errorEl.textContent = data.message || 'รหัสผิดหรือเข้าสู่ระบบไม่ได้';
                errorEl.style.display = 'block';
                btnLogin.disabled = false;
                btnLogin.textContent = "ยืนยัน";
            }
        } catch (err) {
            console.error("Error:", err);
            errorEl.textContent = 'ติดต่อเซิร์ฟเวอร์ไม่ได้';
            errorEl.style.display = 'block';
            btnLogin.disabled = false;
            btnLogin.textContent = "ยืนยัน";
        }
    });
});