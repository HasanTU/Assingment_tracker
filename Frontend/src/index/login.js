document.addEventListener("DOMContentLoaded", () => {
    const btnLogin = document.getElementById("btn-login");
    
    // ตรวจสอบเบื้องต้นว่าเจอตัวแปรไหม
    console.log("Config URL:", APP.CONFIG.BACKEND_API_URL);

    if (btnLogin) {
        btnLogin.addEventListener("click", async (e) => {
            e.preventDefault();
            console.log("Button clicked! Attempting to login...");

            const username = document.getElementById("input-username").value.trim();
            const password = document.getElementById("input-password").value.trim();

            if (!username || !password) {
                alert("กรุณากรอกรหัสนักศึกษาและรหัสผ่าน");
                return;
            }

           try {
    console.log("Starting fetch..."); // เพิ่มบรรทัดนี้
    const response = await fetch(`${APP.CONFIG.BACKEND_API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
        credentials: "include"
    });

    console.log("Response received:", response.status); // เพิ่มบรรทัดนี้
    const data = await response.json();
    console.log("Data parsed:", data); // เพิ่มบรรทัดนี้

    if (response.ok) {
        window.location.href = "../home.html";
    } else {
        alert(data.error || "Login ไม่สำเร็จ");
    }
} catch (err) {
    console.error("Fetch Error Detail:", err); // ดู Error แบบละเอียด
    alert("ติดต่อ Server ไม่ได้: " + err.message);
}
        });
    } else {
        console.error("หาปุ่ม btn-login ไม่เจอ!");
    }
});