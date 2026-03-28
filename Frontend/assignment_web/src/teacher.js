async function createAssignment() {
    const title = document.getElementById("input-title").value;
    const deadline = document.getElementById("input-deadline").value;

    if (!title || !deadline) {
        alert("กรอกข้อมูลให้ครบ");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/api/assignments/create", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                title: title,
                deadline: deadline,
                description: ""
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "error");
        }

        uploadFile('teacher-file', 'teacher')

        alert("สร้างงานเรียบร้อย!");
    } catch (err) {
        console.error(err);
        alert("สร้างไม่สำเร็จ");
    }
}