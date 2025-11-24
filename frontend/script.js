document.addEventListener("DOMContentLoaded", async () => {
    const form = document.getElementById("calcForm");
    const resultDiv = document.getElementById("result");
    const beltSelect = document.getElementById("belt_select");

    // Загрузка списка ремней из БД
    try {
        const response = await fetch("http://127.0.0.1:8000/belts");
        const belts = await response.json();
        beltSelect.innerHTML = belts.map(b => `<option value="${b.id}">${b.designation} (${b.belt_type === 'v_belt' ? 'Клиновой' : 'Поликлиновой'})</option>`).join('');
    } catch (err) {
        beltSelect.innerHTML = '<option value="">Ошибка загрузки ремней</option>';
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        resultDiv.style.display = "none";
        resultDiv.innerHTML = "<p>Расчёт…</p>";

        const data = {
            belt_id: parseInt(beltSelect.value),
            F: parseFloat(document.getElementById("F").value),
            Z: parseFloat(document.getElementById("Z").value),
            fi: parseFloat(document.getElementById("fi").value),
            C1: parseFloat(document.getElementById("C1").value),
            C3: parseFloat(document.getElementById("C3").value),
            X: parseFloat(document.getElementById("X").value),
            v: parseFloat(document.getElementById("v").value),
            alpha1: parseFloat(document.getElementById("alpha1").value),
            gamma1: parseFloat(document.getElementById("gamma1").value)
        };

        try {
            const response = await fetch("http://127.0.0.1:8000/calculate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (!response.ok) throw new Error("Ошибка расчёта");

            const result = await response.json();

            resultDiv.innerHTML = `
                <h2>Результаты для ${result.designation} (${result.belt_type})</h2>
                <table>
                    <tr><td>Рабочее σ, МПа</td><td>${result.working_sigma_MPa}</td></tr>
                    <tr><td>Допустимое [σ0], МПа</td><td>${result.sigma_0_allowed_MPa}</td></tr>
                    <tr><td>Q₀, Н</td><td>${result.Q0_N}</td></tr>
                    <tr><td>R, мм</td><td>${result.R_mm}</td></tr>
                    <tr><td>tg θ</td><td>${result.tg_theta}</td></tr>
                    <tr><td>θ, °</td><td>${result.theta_deg}</td></tr>
                </table>
            `;
            resultDiv.style.display = "block";
        } catch (err) {
            resultDiv.innerHTML = `<p style="color:red">Ошибка: ${err.message}</p>`;
            resultDiv.style.display = "block";
        }
    });
});