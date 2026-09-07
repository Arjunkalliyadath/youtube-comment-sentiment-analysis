(function () {
  "use strict";

  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  /* -----------------------------------------------------------------
     Count up the total-comments number on load
     ----------------------------------------------------------------- */
  function animateCount(el) {
    const target = parseInt(el.dataset.count, 10) || 0;

    if (prefersReducedMotion || target === 0) {
      el.textContent = target.toLocaleString();
      return;
    }

    const duration = 900;
    const start = performance.now();

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(eased * target).toLocaleString();
      if (progress < 1) requestAnimationFrame(tick);
    }

    requestAnimationFrame(tick);
  }

  document.querySelectorAll(".pulse-total").forEach(animateCount);

  /* -----------------------------------------------------------------
     Fill the sentiment spectrum bar to its target width
     ----------------------------------------------------------------- */
  const segments = document.querySelectorAll(".spectrum-segment");
  if (segments.length) {
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        segments.forEach((seg) => {
          seg.style.width = (seg.dataset.pct || 0) + "%";
        });
      });
    });
  }

  /* -----------------------------------------------------------------
     Comment explorer tabs
     ----------------------------------------------------------------- */
  const tabs = document.querySelectorAll(".tab");
  const panels = document.querySelectorAll(".panel");

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const target = tab.dataset.tab;

      tabs.forEach((t) => {
        t.classList.toggle("active", t === tab);
        t.setAttribute("aria-selected", t === tab ? "true" : "false");
      });

      panels.forEach((panel) => {
        panel.classList.toggle("active", panel.dataset.panel === target);
      });
    });
  });

  /* -----------------------------------------------------------------
     Hero particle field — a quiet constellation drifting behind the
     video card and pulse stats. Skipped entirely for reduced motion.
     ----------------------------------------------------------------- */
  const canvas = document.getElementById("hero-field");
  if (!canvas || prefersReducedMotion) return;

  const ctx = canvas.getContext("2d");
  const hero = canvas.closest(".hero");
  const colors = ["rgba(0,229,199,", "rgba(123,97,255,", "rgba(255,61,129,"];

  let particles = [];
  let width = 0;
  let height = 0;
  let animationId = null;

  function resize() {
    width = hero.clientWidth;
    height = hero.clientHeight;
    canvas.width = width * window.devicePixelRatio;
    canvas.height = height * window.devicePixelRatio;
    canvas.style.width = width + "px";
    canvas.style.height = height + "px";
    ctx.setTransform(window.devicePixelRatio, 0, 0, window.devicePixelRatio, 0, 0);

    const count = Math.min(46, Math.round((width * height) / 18000));
    particles = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.25,
      vy: (Math.random() - 0.5) * 0.25,
      r: Math.random() * 1.6 + 0.6,
      color: colors[Math.floor(Math.random() * colors.length)],
    }));
  }

  function step() {
    ctx.clearRect(0, 0, width, height);

    particles.forEach((p) => {
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0 || p.x > width) p.vx *= -1;
      if (p.y < 0 || p.y > height) p.vy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = p.color + "0.75)";
      ctx.fill();
    });

    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const a = particles[i];
        const b = particles[j];
        const dist = Math.hypot(a.x - b.x, a.y - b.y);

        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = `rgba(123,97,255,${0.12 * (1 - dist / 120)})`;
          ctx.lineWidth = 1;
          ctx.stroke();
        }
      }
    }

    animationId = requestAnimationFrame(step);
  }

  window.addEventListener("resize", () => {
    cancelAnimationFrame(animationId);
    resize();
    step();
  });

  resize();
  step();
})();
