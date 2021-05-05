function getQRCode() {
    let xhttp = new XMLHttpRequest();
    let fullname = document.getElementById("fullname").value;
    let phone_number = document.getElementById("phone_number").value;
    let email = document.getElementById("email").value;

    if (!fullname || !phone_number | !email) {
        alert("Vui lòng nhập đủ thông tin.");
        return;
    }

    let phone_regex = "(\\+84[3|5|7|8|9])+([0-9]{8})|(0[3|5|7|8|9])+([0-9]{8})\\b"
    if (!phone_number.match(phone_regex)) {
        alert("Số điện thoại không đúng định dạng. Vui lòng nhập lại.");
        return;
    }

    let data = {
        "fullname": fullname,
        "phone_number": phone_number,
        "email": email
    };

    let qr_container = document.getElementById("qrcode_container");
    qr_container.innerHTML = "";

    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            let resp = JSON.parse(this.responseText);

            if (resp.code !== "00") {
                console.log(resp.code);
                console.log(resp);
                showError(resp.message);
            } else {
                showQRcode(resp.data.filename, qr_container);
            }
        }
    };
    xhttp.open("POST", "/generate", true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify(data));
}

function showQRcode(filename, container) {
    container.hidden = false;

    let p = document.createElement("p");
    p.innerText = "Đây là QR Code của bạn";

    let img = document.createElement("img");
    img.setAttribute("src", "/static/" + filename);
    img.setAttribute("atl", "QR Code");
    img.setAttribute("width", "300px");
    img.setAttribute("height", "300px");
    img.style.border = "1px solid #555";

    container.appendChild(p);
    container.appendChild(img);
}

function showError(message) {
    let error_container = document.getElementById("error_container");
    error_container.hidden = false;
    error_container.innerHTML = "";
    let p = document.createElement("p");
    p.setAttribute("class", "error");
    p.innerText = message;

    error_container.appendChild(p);
}