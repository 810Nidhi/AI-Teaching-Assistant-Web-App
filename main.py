from hf import generate_response
import re
import streamlit as st 
def looks_incomplete(text:str)->bool:
    if not text or len(text.strip())<10:
        return True
    t=text.strip()
    if t.endswith(("**","*","-","_",":",",","(","[","{")):
        return True
    if re.search(r"\d+\.\s*$",t):
        return True
    if not re.search(r"[.!?]$",t):
        return True
    return False
def complete_answer(question:str,max_rounds:int=2)->str:
    base_prompt=(
        "Answer clearly in numbered points"
        "Do not cut the sentences.Finish each point fully\n\n"
        f"Question:{question}"
    )
    ans=generate_response(base_prompt,temperature=0.3,max_tokens=1024)
    rounds=0
    while rounds<max_rounds and looks_incomplete(ans):
        cont_prompt=(
            "Continue exactly from where you first stopped "
            "Do not repeat the previous text"
            "Finish the incomplete point and complete the answer.\n\n"
            f"Questions:{question}\n\n"
            f"Answers so far:{ans}\n\n"
        )
        more=generate_response(cont_prompt,temperature=0.3,max_tokens=1024)
        if not more or more.strip() in ans:
            break
        ans=ans.rstrip()+"\n"+more.lstrip().strip()
        rounds+=1
    return ans
def main():
    st.title("AI teaching Assistant")
    st.write("Welcome You can ask questions and get answers.")
    user_input=st.text_area("Ask your question here:")
    if user_input:
        st.write(f"**Your question:** {user_input}")
        response=complete_answer(user_input)
        st.write("**Answer:**")
        st.markdown(response)
    else:
        st.info("Please enter a question to get an answer.")
if __name__=="__main__":
    main()