import streamlit as st
import speedtest
import socket

st.set_page_config(page_title="Testador de Conexão", layout="centered")

st.markdown("## 🌐 Testador de Conexão de Internet")

if st.button("🚀 Iniciar Teste de Conexão"):
    with st.spinner("⏳ Testando conexão..."):
        try:
            # Verifica se há internet
            socket.create_connection(("www.google.com", 80), timeout=5)
            st.success("✅ Conectado à Internet")

            # Faz o teste de velocidade
            stt = speedtest.Speedtest()
            stt.get_best_server()
            download = stt.download()
            upload = stt.upload()
            ping = stt.results.ping

            st.markdown(f"🔻 **Download:** `{download / 1_000_000:.2f} Mbps`")
            st.markdown(f"🔺 **Upload:** `{upload / 1_000_000:.2f} Mbps`")
            st.markdown(f"📡 **Ping:** `{ping:.0f} ms`")

        except:
            st.error("❌ Sem conexão ou erro no teste")



