const apiver = $("#apiVersion");
const stdlibver = $("#stdlibVersion");
const codeEditor = $("#ktcode");
const runButton = $("#run");
const codeStatus = $("#status");

const moon = `<svg fill="white" xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 384 512"><path d="M223.5 32C100 32 0 132.3 0 256S100 480 223.5 480c60.6 0 115.5-24.2 155.8-63.4c5-4.9 6.3-12.5 3.1-18.7s-10.1-9.7-17-8.5c-9.8 1.7-19.8 2.6-30.1 2.6c-96.9 0-175.5-78.8-175.5-176c0-65.8 36-123.1 89.3-153.3c6.1-3.5 9.2-10.5 7.7-17.3s-7.3-11.9-14.3-12.5c-6.3-.5-12.6-.8-19-.8z"/></svg>`;
const sun = `<svg fill="white" xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><path d="M361.5 1.2c5 2.1 8.6 6.6 9.6 11.9L391 121l107.9 19.8c5.3 1 9.8 4.6 11.9 9.6s1.5 10.7-1.6 15.2L446.9 256l62.3 90.3c3.1 4.5 3.7 10.2 1.6 15.2s-6.6 8.6-11.9 9.6L391 391 371.1 498.9c-1 5.3-4.6 9.8-9.6 11.9s-10.7 1.5-15.2-1.6L256 446.9l-90.3 62.3c-4.5 3.1-10.2 3.7-15.2 1.6s-8.6-6.6-9.6-11.9L121 391 13.1 371.1c-5.3-1-9.8-4.6-11.9-9.6s-1.5-10.7 1.6-15.2L65.1 256 2.8 165.7c-3.1-4.5-3.7-10.2-1.6-15.2s6.6-8.6 11.9-9.6L121 121 140.9 13.1c1-5.3 4.6-9.8 9.6-11.9s10.7-1.5 15.2 1.6L256 65.1 346.3 2.8c4.5-3.1 10.2-3.7 15.2-1.6zM160 256a96 96 0 1 1 192 0 96 96 0 1 1 -192 0zm224 0a128 128 0 1 0 -256 0 128 128 0 1 0 256 0z"/></svg>`;
const xmark = `<svg fill="red" xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 384 512"><path d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"/></svg>`;
const ymark = `<svg fill="green" xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512"><path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z"/></svg>`;

const loadingAnimation = `<div class="lds-dual-ring">`;

fetch("/api/version").then((response) => {
  response.json().then((data) => {
    if (data.error) {
      console.log(data.error);

      apiver.text("API: OFFLINE");
      stdlibver.text("ERROR: " + data.error);

      apiver.removeClass("bg-primary").addClass("bg-warning");
      stdlibver.removeClass("bg-primary").addClass("bg-danger");
    } else {
      apiver.text("API: ONLINE");
      stdlibver.text("STDLIB Version: " + data[0].stdlibVersion);

      stdlibver.removeClass("bg-primary").addClass("bg-success");
      runButton.prop("disabled", false);
    }
  });
});

function runCode() {
  runButton.prop("disabled", true);
  codeStatus.html(loadingAnimation);

  let startTime = new Date().getTime();

  let code = codeEditor.val();
  fetch("/api/run?code=" + btoa(code), {}).then((response) => {
    response.json().then((data) => {
      $("#output").empty();
      if (data.error) {
        $("#output").append(`<div class="alert alert-danger p-0" role="alert">
                <p>${data.error}</p>
                </div>`);
        codeStatus.html(xmark);
      } else {
        $("#output").append(`<div class="alert alert-success p-0" role="alert">
                <p>${data.message}</p>
                </div>`);
        let timeDiff = new Date().getTime() - startTime;
        codeStatus.html(ymark + " Compiled in " + timeDiff + "ms");
      }
    });

    runButton.prop("disabled", false);
  });
}

codeEditor.text(`fun main() {
  println("Hello, World!")
}`);

let darkEnabled = JSON.parse(localStorage.getItem("darkmode"));

if (darkEnabled === null) {
  localStorage.setItem("darkmode", true);
  darkEnabled = true;
}

function toggleDarkMode() {
  if (darkEnabled) {
    $("#darkmode").html(moon);
    $("html").attr("data-bs-theme", "light");
  } else {
    $("#darkmode").html(sun);
    $("html").attr("data-bs-theme", "dark");
  }
}

$("#darkmode_btn").click(() => {
  darkEnabled = !darkEnabled;
  if (darkEnabled) localStorage.setItem("darkmode", true);
  else localStorage.setItem("darkmode", false);
  toggleDarkMode();
});

toggleDarkMode();

runButton.click(() => {
  runCode();
});
