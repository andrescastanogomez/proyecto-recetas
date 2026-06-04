const API_URL = "";
let token = localStorage.getItem("token") || "";

document.addEventListener("DOMContentLoaded", () => {
    if (token) {
        showApp();
    }
});

async function register() {
    const email = document.getElementById("auth-email").value.trim();
    const password = document.getElementById("auth-password").value;

    const res = await fetch(`${API_URL}/api/auth/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: email,
            password: password
        })
    });

    const data = await res.json().catch(() => ({}));

    if (res.ok) {
        alert("Registro exitoso");
    } else {
        alert(data.detail || "Error al registrar");
    }
}

async function login() {
    const email = document.getElementById("auth-email").value.trim();
    const password = document.getElementById("auth-password").value;

    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const res = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formData
    });

    const data = await res.json().catch(() => ({}));

    if (res.ok) {
        token = data.access_token;
        localStorage.setItem("token", token);
        showApp();
    } else {
        alert(data.detail || "Login incorrecto");
    }
}

function logout() {
    localStorage.removeItem("token");
    token = "";

    document.getElementById("auth-section").style.display = "block";
    document.getElementById("app-content").style.display = "none";
    document.getElementById("logout-btn").style.display = "none";
}

function showApp() {
    document.getElementById("auth-section").style.display = "none";
    document.getElementById("app-content").style.display = "block";
    document.getElementById("logout-btn").style.display = "block";

    loadIngredients();
    loadHistory();
}

async function loadIngredients() {
    const res = await fetch(`${API_URL}/api/ingredientes/`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });

    if (!res.ok) {
        console.error("Error ingredientes:", await res.text());
        return;
    }

    const ingredientes = await res.json();

    const list = document.getElementById("ingredients-list");
    const selection = document.getElementById("ingredients-selection");

    list.innerHTML = "";
    selection.innerHTML = "";

    ingredientes.forEach(ing => {
        const li = document.createElement("li");

        const nombreSeguro = JSON.stringify(ing.nombre ?? "");
        const cantidadSegura = JSON.stringify(String(ing.cantidad ?? ""));

        li.innerHTML = `
            <strong>${ing.nombre ?? ""}</strong>
            (${ing.cantidad ?? ""})

            <button onclick='updateIngredientPrompt(${ing.id}, ${nombreSeguro}, ${cantidadSegura})'>
                Editar
            </button>

            <button onclick="deleteIngredient(${ing.id})">
                Eliminar
            </button>
        `;

        list.appendChild(li);

        selection.innerHTML += `
            <label style="display:block;margin-bottom:8px;">
                <input
                    type="checkbox"
                    value="${ing.id}"
                    data-name="${ing.nombre ?? ""}"
                    checked
                >
                ${ing.nombre ?? ""} (${ing.cantidad ?? ""})
            </label>
        `;
    });
}

async function addIngredient() {
    const nombre = document.getElementById("ing-name").value.trim();
    const cantidad = document.getElementById("ing-qty").value.trim();

    if (!nombre) {
        alert("Ingrese un nombre");
        return;
    }

    if (!cantidad) {
        alert("Cantidad inválida");
        return;
    }

    const payload = {
        nombre: nombre,
        cantidad: Number(cantidad)
    };

    console.log("Payload addIngredient:", payload);

    const res = await fetch(`${API_URL}/api/ingredientes/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    });

    const data = await res.json().catch(() => ({}));

    if (res.ok) {
        document.getElementById("ing-name").value = "";
        document.getElementById("ing-qty").value = "";
        loadIngredients();
    } else {
        console.error("Error addIngredient:", data);
        alert(JSON.stringify(data.detail || data || "Error agregando ingrediente"));
    }
}

async function updateIngredientPrompt(id, nombre, cantidadActual) {
    const nuevaCantidad = prompt(`Nueva cantidad para ${nombre}`, String(cantidadActual ?? ""));

    if (nuevaCantidad === null) return;

    const cantidadLimpia = nuevaCantidad.trim();

    if (!cantidadLimpia) {
        alert("Cantidad inválida");
        return;
    }

    const payload = {
        nombre: String(nombre),
        cantidad: Number(cantidadLimpia)
    };

    console.log("Payload updateIngredient:", payload);

    const res = await fetch(`${API_URL}/api/ingredientes/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    });

    const data = await res.json().catch(() => ({}));

    if (res.ok) {
        loadIngredients();
    } else {
        console.error("Error updateIngredientPrompt:", data);
        alert(JSON.stringify(data.detail || data || "Error actualizando ingrediente"));
    }
}

async function deleteIngredient(id) {
    if (!confirm("¿Eliminar ingrediente?")) return;

    const res = await fetch(`${API_URL}/api/ingredientes/${id}`, {
        method: "DELETE",
        headers: {
            Authorization: `Bearer ${token}`
        }
    });

    if (res.ok) {
        loadIngredients();
    } else {
        const data = await res.json().catch(() => ({}));
        console.error("Error deleteIngredient:", data);
        alert(JSON.stringify(data.detail || data || "Error eliminando ingrediente"));
    }
}

async function generateRecipe() {
    const res = await fetch(`${API_URL}/api/recetas/generar`, {
        method: "POST",
        headers: {
            Authorization: `Bearer ${token}`
        }
    });

    const receta = await res.json().catch(() => ({}));

    if (!res.ok) {
        alert(receta.detail || "Error generando receta");
        return;
    }

    document.getElementById("recipe-title").innerText = receta.nombre || "";
    document.getElementById("recipe-steps").innerText = receta.pasos || "";
    document.getElementById("recipe-time").innerText = receta.tiempo_estimado || "";
    document.getElementById("recipe-diff").innerText = receta.dificultad || "";

    const ingredientesElement = document.getElementById("recipe-ingredients");
    let ingredientes = receta.ingredientes_receta || receta.ingredientes || [];

    if (typeof ingredientes === "string") {
        try {
            ingredientes = JSON.parse(ingredientes);
        } catch {
            ingredientes = [ingredientes];
        }
    }

    ingredientesElement.innerHTML = Array.isArray(ingredientes)
        ? `<ul>${ingredientes.map(i => `<li>${i}</li>`).join("")}</ul>`
        : ingredientes;

    document.getElementById("recipe-result").style.display = "block";
    loadHistory();
}

/* 🔄 MODIFICACIÓN AQUÍ: Carga el historial renderizando 5 estrellas interactivas */
async function loadHistory() {
    const res = await fetch(`${API_URL}/api/recetas/`, {
        headers: { Authorization: `Bearer ${token}` }
    });

    if (!res.ok) return;

    const recetas = await res.json();
    const historyDiv = document.getElementById("recipes-history");

    historyDiv.innerHTML = "";

    recetas.forEach(rec => {
        const div = document.createElement("div");
        div.style.borderBottom = "1px solid #e2e8f0";
        div.style.paddingBottom = "1rem";
        div.style.marginBottom = "1rem";

        div.innerHTML = `
            <h4>${rec.nombre}</h4>
            <p style="margin:4px 0; font-size:0.9rem; color:#64748b;">⚡ Dificultad: ${rec.dificultad || "N/A"}</p>
            <p style="margin:4px 0; font-size:0.9rem; color:#64748b;">⏱️ Tiempo: ${rec.tiempo_estimado || "N/A"}</p>

            <div id="stars-container-${rec.id}" style="margin-top:8px;">
                ${[1, 2, 3, 4, 5].map(estrella => `
                    <span 
                        class="star-btn" 
                        onclick="calificarReceta(${rec.id}, ${estrella})"
                        style="cursor:pointer; font-size:1.3rem; margin-right:4px;"
                        title="Calificar con ${estrella} estrellas">⭐</span>
                `).join("")}
            </div>
        `;

        historyDiv.appendChild(div);
    });
}

/* 🔄 MODIFICACIÓN AQUÍ: Lógica dinámica de votación con bloqueo definitivo */
async function calificarReceta(recetaId, puntos) {
    const contenedor = document.getElementById(`stars-container-${recetaId}`);

    // 🔒 Control de fraude: Detiene la ejecución si ya fue clickeado antes en esta carga
    if (contenedor.getAttribute("data-calificada") === "true") {
        alert("Ya has calificado esta receta. ¡No puedes cambiar tu opinión!");
        return;
    }

    const res = await fetch(`${API_URL}/api/recetas/${recetaId}/calificar`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ puntos: puntos })
    });

    const data = await res.json().catch(() => ({}));

    if (res.ok) {
        // 🔒 Bloqueo lógico inmediato
        contenedor.setAttribute("data-calificada", "true");

        // Bloqueo visual: Apaga las estrellas no seleccionadas y quita el cursor pointer
        const estrellas = contenedor.querySelectorAll(".star-btn");
        estrellas.forEach((est, index) => {
            if (index >= puntos) {
                est.style.opacity = "0.3"; // Apaga las estrellas que quedaron por encima
            }
            est.style.cursor = "not-allowed"; // Indica visualmente que está congelado
        });

        alert(`¡Gracias! Calificaste esta receta con ${puntos} estrellas.`);
    } else {
        alert(data.detail || "Error al calificar");
    }
}