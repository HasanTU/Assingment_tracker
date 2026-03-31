import { CONFIG } from './config.js';

async function checkAuthAndRedirect() {
    const hasToken = document.cookie.split(';').some((item) => item.trim().startsWith('token='));

    // ถ้าไม่มี Cookie เลย ก็ไม่ต้องยิง Fetch ให้เกิด Error ใน Console
    if (!hasToken) {
        console.log("No token found, staying on login page.");
        return; 
    }

    try {
        const response = await fetch(`${CONFIG.BACKEND_API_URL}/login`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include"
        });

        if (response.ok) {
            const data = await response.json();
            
            // ตรวจสอบ Role และเด้งไปหน้าที่ถูกต้อง
            if (data.role === "teacher") {
                window.location.href = "teacher.html";
            } else if (data.role === "student") {
                window.location.href = "student.html";
            }
        }
    } catch (error) {
        console.log("ยังไม่ได้ Login หรือ Token หมดอายุ:", error);
    }
}

checkAuthAndRedirect();


document.addEventListener("DOMContentLoaded", () => {
    const btnLogin = document.getElementById("btn-login");


    btnLogin.addEventListener("click", async (e) => {
        e.preventDefault();

        const username = document.getElementById("input-username").value;
        const password = document.getElementById("input-password").value;
 
        try {
            const response = await fetch(`${CONFIG.BACKEND_API_URL}/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({"username": username, "password":password}),
                credentials: "include"
            });

            const data = await response.json();
            if (!response.ok) {
                alert(data.error || "Login failed");
                return;
            }
            
            const role = data.role
            // login สำเร็จ → redirect
            window.location.href = role + ".html";

        } catch (err) {
            console.error(err);
            alert("เกิดข้อผิดพลาด");
        }
        

    });
});