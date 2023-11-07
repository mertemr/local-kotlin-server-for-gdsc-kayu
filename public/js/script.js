
fetch('/api/version').then((response) => {
    response.json().then((data) => {
        if (data.error) {
            console.log(data.error);
        } else {
            console.log(data);
            $("#apiVersion").append(data[0].version);
            $("#stdlibVersion").append(data[0].stdlibVersion);
        }
    });
});

function runCode() {
    let code = $("#ktcode").val();
    console.log(code);
    fetch("/api/run?code=" + btoa(code), {
    }).then((response) => {
        $("#output").empty();
        response.json().then((data) => {
            console.log(data);
            $("#output").append(data);
        });
    });
}