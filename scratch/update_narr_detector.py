with open('pages/2_Complaint_Classification.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = 'narr_candidates = [c for c in batch_df.columns if "narrative" in c.lower() or "text" in c.lower() or "complaint" in c.lower()]'
replacement = 'narr_candidates = [c for c in batch_df.columns if ("narrative" in c.lower() or "text" in c.lower() or "desc" in c.lower()) and "id" not in c.lower()] or [c for c in batch_df.columns if "complaint" in c.lower() and "id" not in c.lower()]'

assert target in content, 'Target not found in content'
new_content = content.replace(target, replacement)
with open('pages/2_Complaint_Classification.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Successfully updated column auto-detection in 2_Complaint_Classification.py')

