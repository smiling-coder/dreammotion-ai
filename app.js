const API = "http://localhost:8000/api";
const $ = s => document.querySelector(s);
let token = localStorage.getItem("dm_token"), signup = false;

function toast(m){const t=$("#toast");t.textContent=m;t.style.display="block";setTimeout(()=>t.style.display="none",3500)}
async function api(path,opt={}){
  let r;
  try{r=await fetch(API+path,{...opt,headers:{"Content-Type":"application/json",...(token?{Authorization:"Bearer "+token}:{})}})}
  catch{throw new Error("Cannot reach the server. Start the backend first.")}
  const d=await r.json().catch(()=>({}));
  if(!r.ok) throw new Error(typeof d.detail==="string"?d.detail:"Something went wrong. Check your input.");
  return d;
}
$("#theme").onclick=()=>{const h=document.documentElement;h.dataset.theme=h.dataset.theme==="dark"?"light":"dark"};
const open=v=>$("#modal").classList.toggle("open",v);
$("#authBtn").onclick=()=>{ if(token){token=null;localStorage.removeItem("dm_token");location.reload()} else open(true) };
$("#close").onclick=()=>open(false);
$("#swap").onclick=()=>{signup=!signup;$("#authTitle").textContent=signup?"Create account":"Log in";$("#swap").textContent=signup?"Have an account? Log in":"New here? Create an account"};
$("#authForm").onsubmit=async e=>{e.preventDefault();
  try{const d=await api(signup?"/register":"/login",{method:"POST",body:JSON.stringify({email:$("#em").value,password:$("#pw").value})});
    token=d.token;localStorage.setItem("dm_token",token);open(false);toast("Welcome to DreamMotion AI");init();
  }catch(err){toast(err.message)}};
$("#promptForm").onsubmit=async e=>{e.preventDefault();
  if(!token){toast("Log in to save your idea as a project.");open(true);return}
  try{const v=$("#promptIn").value;await api("/projects",{method:"POST",body:JSON.stringify({title:v.slice(0,60)||"Untitled",prompt:v})});
    $("#promptIn").value="";toast("Project saved as a draft.");init();
  }catch(err){toast(err.message)}};
async function init(){
  $("#authBtn").textContent=token?"Log out":"Log in";
  if(!token) return;
  try{const list=await api("/projects");$("#projects").hidden=false;
    const box=$("#plist");box.innerHTML="";
    if(!list.length) box.innerHTML='<div class="card"><p>No projects yet. Describe a video above to start.</p></div>';
    list.forEach(p=>{const c=document.createElement("div");c.className="card proj";
      const s=document.createElement("span");s.textContent=p.title+" ("+p.status+")";
      const b=document.createElement("button");b.textContent="Delete";
      b.onclick=async()=>{await api("/projects/"+p.id,{method:"DELETE"});init()};
      c.append(s,b);box.append(c)});
  }catch(err){toast(err.message)}
}
document.querySelectorAll(".frame").forEach(f=>{
  f.onpointerdown=e=>{f.setPointerCapture(e.pointerId);const st=$("#stage").getBoundingClientRect(),r=f.getBoundingClientRect(),dx=e.clientX-r.left,dy=e.clientY-r.top;
    f.onpointermove=m=>{f.style.left=Math.max(0,Math.min(st.width-r.width,m.clientX-st.left-dx))+"px";f.style.top=Math.max(0,Math.min(st.height-r.height,m.clientY-st.top-dy))+"px"};
    f.onpointerup=()=>{f.onpointermove=null}}});
addEventListener("pointermove",e=>{const g=$("#glow");g.style.left=e.clientX+"px";g.style.top=e.clientY+"px"});
init();
