function getQRCode() {
    let xhttp = new XMLHttpRequest();
    let fullname = document.getElementById("fullname").value;
    let phone_number = document.getElementById("phone_number").value;
    let email = document.getElementById("email").value;
    let address = document.getElementById("address").value;
    if (!fullname || !phone_number | !email) {
        alert("Vui lòng nhập đủ thông tin.");
        return;
    }

    phone_number = phone_number.replace("+84", "0")
    console.log(phone_number);
    let phone_regex = "(0[3|5|7|8|9])+([0-9]{8})\\b"
    if (!phone_number.match(phone_regex)) {
        alert("Số điện thoại không đúng định dạng. Vui lòng nhập lại.");
        return;
    }


    let data = {
        "fullname": fullname,
        "phone_number": phone_number,
        "email": email,
        'address': address
    };
    document.getElementById("error_container").innerHTML = "";
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

function search() {
    let s = document.getElementById("search-field").value.trim();
    let indexes = getCheckedColumn();
    let table = document.getElementById("user-table");
    for (let i = 1; i < table.rows.length; i++) {
        let found = 0;
        let row = table.rows[i].cells;
        for (let j in indexes) {
            let cell_content = row[indexes[j]].innerText.trim();
            if (cell_content !== "Hà Tĩnh" && cell_content !== "Quảng Ninh") {
                console.log(s + " and " + cell_content);
                console.log("vị trí: " + cell_content.includes(s));
            }
            if (cell_content.search(s) !== -1) {
                found = 1
            }
        }
        if (found === 0) {
            table.rows[i].style.display = "none";
        } else {
            table.rows[i].style.display = "table-row";
        }
    }

}

function format_data() {
    let table = document.getElementById("user-table");
    let key = ["fullname", "phone_number", "email", "address"]
    let request = {'data': []};
    for (let i = 1; i < table.rows.length; i++) {
        // let found = 0;
        if (table.rows[i].style.display !== "none") {
            let data = {}
            let row = table.rows[i].cells;
            for (let j = 1; j < row.length; j++) {
                data[key[j - 1]] = row[j].innerText;
            }
            request.data.push(data)
        }
    }

    request = JSON.stringify(request)
    console.log(request);

    document.getElementById("user_data").value = request;
}

function getListCity() {
    let cities = ['Hồ Chí Minh', 'Hà Nội', 'Đà Nẵng', 'Bình Dương', 'Đồng Nai', 'Khánh Hòa', 'Hải Phòng', 'Long An', 'Quảng Nam', 'Bà Rịa Vũng Tàu', 'Đắk Lắk', 'Cần Thơ', 'Bình Thuận  ', 'Lâm Đồng', 'Thừa Thiên Huế', 'Kiên Giang', 'Bắc Ninh', 'Quảng Ninh', 'Thanh Hóa', 'Nghệ An', 'Hải Dương', 'Gia Lai', 'Bình Phước', 'Hưng Yên', 'Bình Định', 'Tiền Giang', 'Thái Bình', 'Bắc Giang', 'Hòa Bình', 'An Giang', 'Vĩnh Phúc', 'Tây Ninh', 'Thái Nguyên', 'Lào Cai', 'Nam Định', 'Quảng Ngãi', 'Bến Tre', 'Đắk Nông', 'Cà Mau', 'Vĩnh Long', 'Ninh Bình', 'Phú Thọ', 'Ninh Thuận', 'Phú Yên', 'Hà Nam', 'Hà Tĩnh', 'Đồng Tháp', 'Sóc Trăng', 'Kon Tum', 'Quảng Bình', 'Quảng Trị', 'Trà Vinh', 'Hậu Giang', 'Sơn La', 'Bạc Liêu', 'Yên Bái', 'Tuyên Quang', 'Điện Biên', 'Lai Châu', 'Lạng Sơn', 'Hà Giang', 'Bắc Kạn', 'Cao Bằng']

    let datata_list = document.getElementById("city_name");

    for (let i = 0; i < cities.length; i++) {
        let option = document.createElement("option");
        option.innerText = cities[i];
        datata_list.appendChild(option);
    }
}

function getChartData() {
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            let resp = JSON.parse(this.responseText);

            if (resp.code === "00") {
                document.getElementById("chart_container").hidden = false;

                console.log(resp.data);
                drawChart(resp.data.address_data, "Thống kê theo thành phố", [["Thành phố", "Số lượng"]], "city_chart");
                drawChart(resp.data.status_data, "Thống kê theo trạng thái", [["Trạng thái", "Số lượng"]], "status_chart");
                document.getElementById("table-container").hidden = true;
            }
        }
    };
    xhttp.open("POST", "/visualize", true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send();
}

function drawChart(data, title, header_data, container_id) {
    let handled_data = header_data;
    for (let key in data) {
        if (data.hasOwnProperty(key)) {
            handled_data.push([key, data[key]])
        }
    }

    var chart_data = google.visualization.arrayToDataTable(handled_data);
    let options = {'title': title, 'width': 550, 'height': 400};

    // Display the chart inside the <div> element with id="piechart"
    let city_chart = new google.visualization.PieChart(document.getElementById(container_id));
    city_chart.draw(chart_data, options);

}

function getCheckedColumn() {
    let filter = document.getElementById("filter_container");
    let index_arr = []
    let checkboxes = filter.querySelectorAll("input")

    for (let i = 0; i < checkboxes.length; i++) {
        // console.log()
        if (checkboxes[i].checked === true) {
            index_arr.push(i + 1);
        }
    }

    if (index_arr.length === 0) {

        for (let i = 0; i < checkboxes.length; i++) {
            // console.log()

            index_arr.push(i + 1);

        }
    }
    // console.log(index_arr)
    return index_arr;

}