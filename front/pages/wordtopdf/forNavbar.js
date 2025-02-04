// Navbarni yuklash
fetch("../../navbar/navbar.html")
    .then(response => response.text())
    .then(data => {
        document.getElementById("navbar-container").innerHTML = data;

        // CSS faylni ham dinamik yuklaymiz
        let link = document.createElement("link");
        link.rel = "stylesheet";
        link.href = "../../navbar/navbar.css"; // CSS fayliga to‘g‘ri yo‘l
        document.head.appendChild(link);
    })
    .catch(error => console.error("Navbar yuklanmadi:", error));