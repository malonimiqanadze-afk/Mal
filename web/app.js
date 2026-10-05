let roomDatabase = {};
let quantities = {};
let activeRoom = null;

function titleCase(key) {
  return key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function itemCount(roomName) {
  const roomQty = quantities[roomName] || {};
  return Object.values(roomQty).reduce((sum, qty) => sum + (qty > 0 ? 1 : 0), 0);
}

function renderTabs() {
  const tabsEl = document.getElementById("room-tabs");
  tabsEl.innerHTML = "";
  Object.keys(roomDatabase).forEach((roomName) => {
    const btn = document.createElement("button");
    btn.className = "tab-btn" + (roomName === activeRoom ? " active" : "");
    btn.innerHTML = `${roomName} <span class="tab-badge">${itemCount(roomName)}</span>`;
    btn.addEventListener("click", () => {
      activeRoom = roomName;
      renderTabs();
      renderItems();
    });
    tabsEl.appendChild(btn);
  });
}

function renderItems() {
  const gridEl = document.getElementById("item-grid");
  gridEl.innerHTML = "";
  const items = roomDatabase[activeRoom] || {};
  Object.entries(items).forEach(([itemKey, volume]) => {
    const qty = quantities[activeRoom][itemKey] || 0;

    const card = document.createElement("div");
    card.className = "item-card";
    card.innerHTML = `
      <div>
        <div class="item-name">${titleCase(itemKey)}</div>
        <div class="item-volume">${volume} cu ft</div>
      </div>
      <div class="stepper">
        <button class="minus" ${qty <= 0 ? "disabled" : ""}>-</button>
        <span class="qty">${qty}</span>
        <button class="plus">+</button>
      </div>
    `;

    card.querySelector(".minus").addEventListener("click", () => {
      quantities[activeRoom][itemKey] = Math.max(0, qty - 1);
      renderTabs();
      renderItems();
    });
    card.querySelector(".plus").addEventListener("click", () => {
      quantities[activeRoom][itemKey] = qty + 1;
      renderTabs();
      renderItems();
    });

    gridEl.appendChild(card);
  });
}

function clearAll() {
  Object.keys(roomDatabase).forEach((roomName) => {
    Object.keys(roomDatabase[roomName]).forEach((itemKey) => {
      quantities[roomName][itemKey] = 0;
    });
  });
  renderTabs();
  renderItems();
}

function setStatus(message, type) {
  const el = document.getElementById("status-message");
  el.textContent = message;
  el.className = type || "";
}

async function handleSubmit(event) {
  event.preventDefault();

  const customerInfo = {
    full_name: document.getElementById("full_name").value.trim(),
    email: document.getElementById("email").value.trim(),
    phone: document.getElementById("phone").value.trim(),
    move_date: document.getElementById("move_date").value.trim(),
    postcode_from: document.getElementById("postcode_from").value.trim(),
    postcode_to: document.getElementById("postcode_to").value.trim(),
    access_notes: document.getElementById("access_notes").value.trim(),
  };

  if (!customerInfo.full_name || !customerInfo.email) {
    setStatus("Full name and email are required.", "error");
    return;
  }

  const saveBtn = document.getElementById("save-btn");
  saveBtn.disabled = true;
  setStatus("Saving quote and sending report...", "");

  try {
    const result = await window.pywebview.api.submit_quote(customerInfo, quantities);
    if (result.ok) {
      setStatus("Quote saved! Report emailed to " + customerInfo.email + ".", "success");
    } else {
      setStatus(result.message || "Something went wrong.", "error");
    }
  } catch (err) {
    setStatus("Error: " + err, "error");
  } finally {
    saveBtn.disabled = false;
  }
}

window.addEventListener("pywebviewready", async () => {
  roomDatabase = await window.pywebview.api.get_room_database();
  Object.keys(roomDatabase).forEach((roomName) => {
    quantities[roomName] = {};
    Object.keys(roomDatabase[roomName]).forEach((itemKey) => {
      quantities[roomName][itemKey] = 0;
    });
  });
  activeRoom = Object.keys(roomDatabase)[0];

  renderTabs();
  renderItems();

  document.getElementById("clear-btn").addEventListener("click", clearAll);
  document.getElementById("customer-form").addEventListener("submit", handleSubmit);
});
