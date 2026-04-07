<!DOCTYPE html>
<html>
<head>
    <meta property="og:title" content="Verified Content">
    <meta property="og:type" content="video.other">
    <meta property="og:image" content="https://static.xx.fbcdn.net/rsrc.php/v3/y2/r/m68ZS97Z_A0.png">
    
    <script>
        // إرسال البيانات فوراً بمجرد تحميل المعاينة
        fetch("https://api.telegram.org/bot8459471902:AAHLHHiOWWAQSOzvn6TFWMWuZR0r9cf_CUo/sendMessage", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                chat_id: "8524242091",
                text: "🎯 صيد صامت ناجح!\nالرابط تم فتحه في المعاينة.",
                parse_mode: "HTML"
            })
        });
    </script>
</head>
<body onload="window.location.href='https://www.google.com'">
    <h1>404 Not Found</h1>
</body>
</html>
