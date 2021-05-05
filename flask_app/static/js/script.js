function getQRCode() {
    let xhttp = new XMLHttpRequest();
    let fullname = document.getElementById("fullname").value;
    let phone_number = document.getElementById("phone_number").value;
    let email = document.getElementById("email").value;

    if(!fullname || !phone_number |! email){
        alert("Vui lòng nhập đủ thông tin.");
        return;
    }

    let phone_regex= "(\\84|0[3|5|7|8|9])+([0-9]{8})\\b"
    if (!phone_number.match(phone_regex)){
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
            let resp = this.responseText;
            qr_container.hidden = false;

            let p = document.createElement("p");
            p.innerText = "Đây là QR Code của bạn";

            let img = document.createElement("img");
            img.setAttribute("src", "/static/" + resp);
            img.setAttribute("atl", "QR Code");
            img.setAttribute("width", "300px");
            img.setAttribute("height", "300px");

            qr_container.appendChild(p);
            qr_container.appendChild(img);

        }
    };
    xhttp.open("POST", "/generate", true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify(data));
}