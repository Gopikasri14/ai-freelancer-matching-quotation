import React, {useEffect, useState} from "react";
import {createRoot} from "react-dom/client";
import "./styles.css";

const API="http://127.0.0.1:8000/api/v1";

function App(){
  const [form,setForm]=useState({title:"",description:"",project_type:"Website",complexity:"Medium",expected_hours:"",deadline_days:7,revisions:2,budget:""});
  const [project,setProject]=useState(null), [matches,setMatches]=useState([]), [selected,setSelected]=useState(null), [quote,setQuote]=useState(null), [loading,setLoading]=useState(false), [error,setError]=useState("");

  const update=(e)=>setForm({...form,[e.target.name]:e.target.value});

  async function createProject(e){
    e.preventDefault(); setError(""); setLoading(true);
    try{
      const body={...form, deadline_days:Number(form.deadline_days), revisions:Number(form.revisions),
        expected_hours:form.expected_hours?Number(form.expected_hours):null, budget:form.budget?Number(form.budget):null};
      const r=await fetch(`${API}/projects`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
      if(!r.ok) throw new Error(await r.text());
      const p=await r.json(); setProject(p);
      const m=await fetch(`${API}/matching/projects/${p.id}`,{method:"POST"});
      if(!m.ok) throw new Error(await m.text());
      setMatches(await m.json()); setQuote(null); setSelected(null);
    }catch(err){setError(err.message)}finally{setLoading(false)}
  }

  async function generateQuote(){
    if(!selected) return;
    setError(""); setLoading(true);
    try{
      const r=await fetch(`${API}/quotations/generate`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({project_id:project.id,freelancer_id:selected.id})});
      if(!r.ok) throw new Error(await r.text());
      setQuote(await r.json());
    }catch(err){setError(err.message)}finally{setLoading(false)}
  }

  return <div className="page">
    <header><div><h1>AI Freelancer Match</h1><p>Requirement matching + quotation optimization</p></div><span className="badge">TF-IDF • XGBoost</span></header>
    <main>
      <section className="card">
        <h2>1. Create Project</h2>
        <form onSubmit={createProject}>
          <input name="title" placeholder="Project title" value={form.title} onChange={update} required/>
          <textarea name="description" placeholder="Describe the requirements, technologies and features..." value={form.description} onChange={update} required/>
          <div className="grid">
            <label>Type<select name="project_type" value={form.project_type} onChange={update}>{["Website","E-commerce","Mobile App","Data Science","NLP","Dashboard","API"].map(x=><option key={x}>{x}</option>)}</select></label>
            <label>Complexity<select name="complexity" value={form.complexity} onChange={update}>{["Low","Medium","High"].map(x=><option key={x}>{x}</option>)}</select></label>
            <label>Expected hours<input name="expected_hours" type="number" min="1" value={form.expected_hours} onChange={update}/></label>
            <label>Deadline days<input name="deadline_days" type="number" min="1" value={form.deadline_days} onChange={update}/></label>
            <label>Revisions<input name="revisions" type="number" min="0" value={form.revisions} onChange={update}/></label>
            <label>Budget (₹)<input name="budget" type="number" min="1" value={form.budget} onChange={update}/></label>
          </div>
          <button disabled={loading}>{loading?"Processing...":"Find Suitable Freelancers"}</button>
        </form>
        {error && <div className="error">{error}</div>}
      </section>

      {matches.length>0 && <section className="card">
        <h2>2. Recommended Freelancers</h2>
        <div className="cards">{matches.map(m=><div className={`person ${selected?.id===m.id?"selected":""}`} key={m.id}>
          <div className="rank">#{m.rank}</div><h3>{m.name}</h3><p>{m.bio}</p>
          <div className="skills">{m.skills.map(s=><span key={s}>{s}</span>)}</div>
          <p><b>{(m.similarity_score*100).toFixed(1)}%</b> requirement similarity</p>
          <p>{m.experience_years} yrs • ₹{m.hourly_rate}/hr</p>
          <button onClick={()=>{setSelected(m);setQuote(null)}}>Select Freelancer</button>
        </div>)}</div>
      </section>}

      {selected && <section className="card">
        <h2>3. Generate AI Quotation</h2>
        <p>Selected: <b>{selected.name}</b></p>
        <button onClick={generateQuote} disabled={loading}>{loading?"Generating...":"Generate Quotation"}</button>
      </section>}

      {quote && <section className="card quote">
        <h2>4. Optimized Quotation</h2>
        <div className="price">₹{quote.final_min_price.toLocaleString()} – ₹{quote.final_max_price.toLocaleString()}</div>
        <div className="grid stats">
          <div><small>Estimated effort</small><b>{quote.effort_min}–{quote.effort_max} hours</b></div>
          <div><small>Base model price</small><b>₹{quote.base_price.toLocaleString()}</b></div>
          <div><small>Included revisions</small><b>{quote.included_revisions}</b></div>
          <div><small>Extra revision</small><b>₹{quote.extra_revision_price.toLocaleString()}</b></div>
        </div>
        <h3>Adjustments</h3>
        <ul>{Object.entries(quote.adjustments).map(([k,v])=><li key={k}>{k.replaceAll("_"," ")}: {v}%</li>)}</ul>
      </section>}
    </main>
  </div>
}
createRoot(document.getElementById("root")).render(<App/>);
