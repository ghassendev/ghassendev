<p align="center">
  <img src="assets/hero.svg" alt="Ghassen Gharsseloui — Laravel / PHP backend developer" width="100%" />
</p>

Freelance **backend developer** from Tunisia. I've spent about 5 years building production systems, mainly with **Laravel / PHP**.
I also work with Python, Symfony, C#/.NET, Vue and Angular. Founder of [ichtirakai.com](https://ichtirakai.com).

#### What I've shipped to production

- **Payments**: gateway integrations for cards, e-wallets and crypto, with webhooks, idempotency and reconciliation
- **Background processing**: Redis and Laravel queues, workers, retries and scheduled jobs
- **Quality**: automated tests with PHPUnit and Pest
- **Ops**: deployments on AWS and Linux VPS with Nginx, PHP-FPM, systemd, Docker, TLS and monitoring

<p align="center">
  <img src="assets/code-shipped.svg" alt="Lines of code by language across my production projects" width="100%" />
</p>

#### How I build backends

```mermaid
flowchart LR
    C([Web & mobile clients]) --> N[Nginx + TLS]
    N --> A[Laravel API]
    A --> DB[(MySQL / PostgreSQL)]
    A --> R[(Redis)]
    R --> W[Queue workers<br/>retries · scheduling]
    W --> P[Payment gateways<br/>cards · e-wallets · crypto]
    P -. webhooks .-> A
    A --> S3[(AWS S3)]
    T[PHPUnit / Pest] -. guards .-> A
```

#### Experience

```mermaid
timeline
    title My path
    2020 – 2022 : Academic and early projects : Symfony, Spring Boot, Angular, Android
    Freelance : Laravel backends for clients in Saudi Arabia, France and Singapore
    2025 – Nov 2026 : Backend developer at KatsCard (Saudi Arabia) : backend services and APIs, payments, production servers
    Today : Founder of ichtirakai.com : open to freelance and remote roles
```

#### Projects

<table>
<tr>
<td width="33%" valign="top"><a href="https://ichtirakai.com"><img src="assets/ichtirakai.jpg" alt="ichtirakai.com" /></a><br/><b><a href="https://ichtirakai.com">ichtirakai.com</a></b><br/><sub>My company. An Arabic store for AI and software subscriptions (ChatGPT, Gemini, CapCut, Microsoft 365…) with crypto payments and fast delivery.</sub></td>
<td width="33%" valign="top"><a href="https://mauss.mooo.com"><img src="assets/kats-screen.jpg" alt="Kats Screen" /></a><br/><b><a href="https://mauss.mooo.com">Kats Screen</a></b><br/><sub>An Arabic streaming platform for movies, series and anime, with profiles and real-time watch parties.</sub></td>
<td width="33%" valign="top"><a href="https://openopc.mooo.com"><img src="assets/1stake.jpg" alt="1Stake" /></a><br/><b><a href="https://openopc.mooo.com">1Stake</a></b><br/><sub>A Laravel online-casino platform that records deposits and withdrawals on the Polygon blockchain.</sub></td>
</tr>
</table>

**Open source:** [tivideo](https://github.com/ghassendev/tivideo) (Quran reels generator: Next.js + Remotion) · [recordedit](https://github.com/ghassendev/recordedit) (AI video montage: Laravel + Python) · [brain](https://github.com/ghassendev/brain) (AI coding-agent control room) · [kick](https://github.com/ghassendev/kick) (Kick OAuth chat app)

#### Activity

<p align="center">
  <img src="assets/activity.svg" alt="Contribution activity over the last 12 months" width="100%" />
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ghassendev/ghassendev/output/github-snake-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/ghassendev/ghassendev/output/github-snake.svg" />
    <img alt="Contribution snake animation" src="https://raw.githubusercontent.com/ghassendev/ghassendev/output/github-snake-dark.svg" width="100%" />
  </picture>
</p>

#### Contact

📫 [ghassengharsseloui@gmail.com](mailto:ghassengharsseloui@gmail.com) · open to freelance and remote backend roles

<sub>Charts are generated from my own data: the language breakdown comes from the code of my production projects, and the activity chart and snake are rebuilt automatically by GitHub Actions in this repo.</sub>
