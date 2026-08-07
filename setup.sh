set -e
mkdir -p "$HOME/.streamlit"
echo "[server]\nheadless = true\nenableCORS = false\nport = $PORT" > "$HOME/.streamlit/config.toml"
