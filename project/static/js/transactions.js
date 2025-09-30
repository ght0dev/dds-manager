async function fetchJSON(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

async function loadSelect(endpoint, el, placeholder) {
  const data = await fetchJSON(`/api/${endpoint}/`);
  el.innerHTML = `<option value="">${placeholder}</option>` +
    data.results.map(i => `<option value="${i.id}">${i.name}</option>`).join("");
}

async function applyFilters(page=1) {
  const params = new URLSearchParams();
  const date_from = document.getElementById("date_from").value;
  const date_to = document.getElementById("date_to").value;
  const type = document.getElementById("type").value;
  const category = document.getElementById("category").value;
  const subcategory = document.getElementById("subcategory").value;
  const status = document.getElementById("status").value;

  if (date_from) params.set("date_from", date_from);
  if (date_to) params.set("date_to", date_to);
  if (type) params.set("type", type);
  if (category) params.set("category", category);
  if (subcategory) params.set("subcategory", subcategory);
  if (status) params.set("status", status);
  params.set("page", page);

  const data = await fetchJSON(`/api/transactions/?${params.toString()}`);
  renderTable(data);
  renderPagination(data);
}

function renderTable(data) {
  const tbody = document.querySelector("#tx-table tbody");
  tbody.innerHTML = data.results.map(tx => `
    <tr>
      <td>${new Date(tx.created_at).toLocaleString()}</td>
      <td>${tx.status ? tx.status : ""}</td>
      <td>${tx.type ? tx.type : ""}</td>
      <td>${tx.category ? tx.category : ""}</td>
      <td>${tx.subcategory ? tx.subcategory : ""}</td>
      <td>${Number(tx.amount).toLocaleString()} ₽</td>
      <td>${tx.comment || ""}</td>
      <td>
        <a class="btn btn-sm btn-primary" href="/transactions/${tx.id}/edit/">Edit</a>
        <button class="btn btn-sm btn-danger" data-id="${tx.id}" onclick="deleteTx(${tx.id})">Del</button>
      </td>
    </tr>
  `).join("");
}

function renderPagination(data) {
  const ul = document.getElementById("pagination");
  ul.innerHTML = "";
  if (!data.count) return;
  const current = data.page || 1;
  // DRF uses next/previous links — we'll parse from those
  if (data.previous) {
    const prev = document.createElement("li");
    prev.className = "page-item";
    prev.innerHTML = `<a class="page-link" href="#" onclick="applyFilters(${current-1});return false;">Prev</a>`;
    ul.appendChild(prev);
  }
  // basic page links (not exact)
  const next = document.createElement("li");
  next.className = "page-item";
  next.innerHTML = `<a class="page-link" href="#" onclick="applyFilters(${current+1});return false;">Next</a>`;
  ul.appendChild(next);
}

async function deleteTx(id) {
  if (!confirm("Удалить запись?")) return;
  const r = await fetch(`/api/transactions/${id}/`, { method: "DELETE", headers: {'X-CSRFToken': getCookie('csrftoken')} });
  if (r.ok) {
    alert("Удалено");
    applyFilters();
  } else {
    alert("Ошибка удаления");
  }
}

// small helper to get CSRF token
function getCookie(name) {
  const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return v ? v.pop() : '';
}

document.addEventListener("DOMContentLoaded", async () => {
  await loadSelect("types", document.getElementById("type"), "Все типы");
  await loadSelect("statuses", document.getElementById("status"), "Все статусы");
  await loadSelect("categories", document.getElementById("category"), "Все категории");
  await loadSelect("subcategories", document.getElementById("subcategory"), "Все подкатегории");

  document.getElementById("apply").addEventListener("click", () => applyFilters());
  applyFilters();
});
