// paste this line by line to get all links from the navbar
// then feed it to the spider's start_urls prop

var elements = document.getElementsByClassName("md-nav__link localLink");

var elementsArr = Array.prototype.slice.call(elements);

var links = elementsArr.map((elem) => {
  return "https://docs.jitterbit.com/" + elem.getAttribute("href");
});

var linksString = JSON.stringify(links);

var blob = new Blob([linksString], { type: "text/plain" });

var link = document.createElement("a");

link.href = URL.createObjectURL(blob);

link.download = "links.txt";

link.click();
