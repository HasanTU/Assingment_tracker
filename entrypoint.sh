# รอให้ SQL Server เริ่มต้นทำงาน (ประมาณ 15-20 วินาที)
# เราจะพยายามเชื่อมต่อด้วย sqlcmd จนกว่าจะสำเร็จ
for i in {1..50};
do
    /opt/mssql-tools18/bin/sqlcmd -S db -U sa -P SuperStrongPass123! -d master -C -i setup.sql
    if [ $? -eq 0 ]
    then
        echo "Database setup completed successfully!"
        break
    else
        echo "SQL Server is not ready yet... waiting (attempt $i)"
        sleep 2
    fi
done