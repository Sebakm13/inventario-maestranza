# inventario-maestranza 

# 🛠️ Sistema de Control de Inventarios - Maestranzas Unidos S.A.

Este es el prototipo funcional (MVP) desarrollado para el control de inventarios de repuestos y componentes críticos en tiempo real.

---

## 🚀 Cómo ejecutar la aplicación (Instrucciones para el Evaluador)

Para levantar este proyecto de forma rápida y sin configuraciones locales, se recomienda utilizar **GitHub Codespaces** directamente desde este repositorio.

### Opción A: Ejecución rápida en la nube (Recomendado)
1. En la parte superior de este repositorio, haga clic en el botón verde **`Code`**.
2. Seleccione la pestaña **`Codespaces`** y haga clic en **`Create codespace on main`**.
3. Una vez abierto el entorno en el navegador, abra una nueva Terminal y ejecute los siguientes comandos:

```bash
# 1. Crear el entorno virtual e instalar las dependencias
python3 -m venv .venv
source .venv/bin/activate
pip install streamlit pandas

# 2. Ejecutar la aplicación
python3 -m streamlit run app.py
