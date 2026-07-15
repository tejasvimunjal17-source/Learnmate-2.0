import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="LearnMate AI Chatbot",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 LearnMate AI")
st.caption("Powered by IBM watsonx Orchestrate")

chat_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
html,body{
margin:0;
padding:0;
width:100%;
height:100%;
overflow:hidden;
}

#root{
width:100%;
height:100%;
}
</style>
</head>

<body>

<div id="root"></div>

<script>

window.wxOConfiguration = {

orchestrationID:"YOUR_ORCHESTRATION_ID",

hostURL:"YOUR_HOST_URL",

rootElementID:"root",

deploymentPlatform:"ibmcloud",

crn:"YOUR_CRN",

chatOptions:{

agentId:"YOUR_AGENT_ID",

agentEnvironmentId:"YOUR_AGENT_ENVIRONMENT_ID"

}

};

setTimeout(function(){

const script=document.createElement("script");

script.src=window.wxOConfiguration.hostURL+"/wxochat/wxoLoader.js?embed=true";

script.onload=function(){

wxoLoader.init();

};

document.head.appendChild(script);

},0);

</script>

</body>
</html>
"""

components.html(chat_html,height=750,scrolling=False)