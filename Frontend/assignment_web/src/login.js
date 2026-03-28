async function checkAuthAndRedirect() {
    const hasToken = document.cookie.split(';').some((item) => item.trim().startsWith('token='));

    // ถ้าไม่มี Cookie เลย ก็ไม่ต้องยิง Fetch ให้เกิด Error ใน Console
    if (!hasToken) {
        console.log("No token found, staying on login page.");
        return; 
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/api/verify-role", {
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
    const btnTeacher = document.getElementById("btn-login-teacher");
    const btnStudent = document.getElementById("btn-login-student");

    btnTeacher.addEventListener("click", async (e) => {
        e.preventDefault();

        const username = document.getElementById("input-username").value;
        const password = document.getElementById("input-password").value;
        
        try {
            const response = await fetch("http://127.0.0.1:5000/api/loginTest", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({"username": username, "password":password }),
                credentials: "include"
            });

            const data = await response.json();
            if (!response.ok) {
                alert(data.error || "Login failed");
                return;
            }

            // login สำเร็จ → redirect
            window.location.href = "teacher.html";

        } catch (err) {
            console.error(err);
            alert("เกิดข้อผิดพลาด");
        }
    });

    btnStudent.addEventListener("click", async (e) => {
        e.preventDefault();

        const username = document.getElementById("input-username").value;
        const password = document.getElementById("input-password").value;
        
        try {
            const response = await fetch("http://127.0.0.1:5000/api/login", {
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

            // login สำเร็จ → redirect
            window.location.href = "student.html";

        } catch (err) {
            console.error(err);
            alert("เกิดข้อผิดพลาด");
        }
        

    });
});