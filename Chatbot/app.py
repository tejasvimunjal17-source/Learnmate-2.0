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

orchestrationID:
"fbf4ce62fa4b472d835ac9afb3ef3200_e7ad8616-b148-4169-9213-0413e10cac69",

hostURL:
"https://au-syd.watson-orchestrate.cloud.ibm.com",

deploymentPlatform:"ibmcloud",

crn:
"crn:v1:bluemix:public:watsonx-orchestrate:au-syd:a/fbf4ce62fa4b472d835ac9afb3ef3200:e7ad8616-b148-4169-9213-0413e10cac69::",

chatOptions:{
    agentId:
    "87fe3ad0-fb0d-4aca-8f7a-78179712c02c",

    agentEnvironmentId:
    "b2f40f9b-452b-43f3-b94c-ec90ca6b39f9"
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