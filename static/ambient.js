document.addEventListener("DOMContentLoaded", () => {

    // Cursor-reactive spotlight
    const glow = document.createElement("div");
    glow.className = "cursor-glow";
    document.body.appendChild(glow);

    window.addEventListener("pointermove", (e) => {
        glow.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
    });

    // Rising particle field
    const field = document.createElement("div");
    field.className = "particles-field";
    document.body.appendChild(field);

    const colors = ["#4FD8FF", "#A855F7"];
    const count = 26;

    for (let i = 0; i < count; i++) {

        const p = document.createElement("span");
        p.className = "particle";

        const size = (Math.random() * 3 + 1.5).toFixed(1);
        const left = (Math.random() * 100).toFixed(1);
        const duration = (Math.random() * 10 + 10).toFixed(1);
        const delay = (Math.random() * -20).toFixed(1);
        const color = colors[i % 2];

        p.style.left = left + "%";
        p.style.width = size + "px";
        p.style.height = size + "px";
        p.style.background = color;
        p.style.animationDuration = duration + "s";
        p.style.animationDelay = delay + "s";

        field.appendChild(p);
    }

});