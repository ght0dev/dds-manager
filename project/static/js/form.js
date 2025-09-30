// universal fetch wrapper
async function fetchJSON(url, opts) {
  const r = await fetch(url, opts);
  if (!r.ok) {
    const text = await r.text();
    throw new Error(text);
  }
  return r.json();
}

function isoLocal(d) {
  const z = new Date(d);
  const off = z.getTimezoneOffset();
  z.setMinutes(z.getMinutes() - off);
  return z.toISOString().slice(0, 16);
}

// load options into <select>
async function loadSelect(endpoint, el, placeholder, params = {}) {
  const q = new URLSearchParams(params).toString();
  const data = await fetch(`/api/${endpoint}/?${q}`).then(r => r.json());
  const items = data.results;  // теперь всегда results

  el.innerHTML = `<option value="">${placeholder}</option>` +
    items.map(i => `<option value="${i.id}">${i.name}</option>`).join("");
}

async function initForm() {
  const urlParts = window.location.pathname.split('/');
  const maybeId = urlParts.includes("edit") ? urlParts[urlParts.length - 2] : null;
  const txId = maybeId && /^\d+$/.test(maybeId) ? maybeId : null;

  const typeEl = document.getElementById("type");
  const categoryEl = document.getElementById("category");
  const subcategoryEl = document.getElementById("subcategory");
  const statusEl = document.getElementById("status");

  await loadSelect("types", typeEl, "Выберите тип");
  await loadSelect("statuses", statusEl, "Выберите статус");
  await loadSelect("categories", categoryEl, "Выберите категорию");
  await loadSelect("subcategories", subcategoryEl, "Выберите подкатегорию");

  // динамическая фильтрация категорий и подкатегорий
  typeEl.addEventListener("change", async () => {
    const typeId = typeEl.value;
    await loadSelect("categories", categoryEl, "Выберите категорию", typeId ? { type: typeId } : {});
    subcategoryEl.innerHTML = `<option value="">Выберите подкатегорию</option>`;
  });

  categoryEl.addEventListener("change", async () => {
    const categoryId = categoryEl.value;
    await loadSelect("subcategories", subcategoryEl, "Выберите подкатегорию", categoryId ? { category: categoryId } : {});
  });

  if (txId) {
    // загрузка транзакции для редактирования
    const tx = await fetch(`/api/transactions/${txId}/`).then(r => r.json());
    document.getElementById("title").innerText = "Редактировать транзакцию";
    document.getElementById("created_at").value = isoLocal(tx.created_at);
    document.getElementById("amount").value = tx.amount;
    document.getElementById("comment").value = tx.comment || "";
    // выставляем selects
    typeEl.value = tx.type;
    await loadSelect("categories", categoryEl, "Выберите категорию", { type: tx.type });
    categoryEl.value = tx.category;
    await loadSelect("subcategories", subcategoryEl, "Выберите подкатегорию", { category: tx.category });
    subcategoryEl.value = tx.subcategory;
    statusEl.value = tx.status;
  }

  document.getElementById("tx-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const createdAtValue = document.getElementById("created_at").value;
    const createdAt = createdAtValue ? new Date(createdAtValue) : new Date();

    const payload = {
      created_at: createdAt.toISOString(),
      type: parseInt(typeEl.value) || null,
      category: parseInt(categoryEl.value) || null,
      subcategory: parseInt(subcategoryEl.value) || null,
      status: parseInt(statusEl.value) || null,
      amount: parseFloat(document.getElementById("amount").value),
      comment: document.getElementById("comment").value || "",
    };

    try {
      if (txId) {
        await fetchJSON(`/api/transactions/${txId}/`, {
          method: "PUT",
          headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie('csrftoken') },
          body: JSON.stringify(payload)
        });
        alert("Сохранено");
        window.location = "/";
      } else {
        await fetchJSON(`/api/transactions/`, {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie('csrftoken') },
          body: JSON.stringify(payload)
        });
        alert("Создано");
        window.location = "/";
      }
    } catch (err) {
      alert("Ошибка: " + err.message);
    }
  });
}

function getCookie(name) {
  const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return v ? v.pop() : '';
}

document.addEventListener("DOMContentLoaded", initForm);
