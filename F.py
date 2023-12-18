import csv
import os
import re
import torch
import tkinter as tk
from tkinter import ttk, messagebox
import seaborn as sns
import matplotlib.pyplot as plt

from PyPDF2 import PdfReader

def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page_text = pdf_reader.pages[page_num].extract_text()
            yield page_text

def process_text(text):

    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    

    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def perform_tensor_operations(text):
    
    words = text.split()
    word_lengths = torch.tensor([len(word) for word in words], dtype=torch.float32)
    return word_lengths

def visualize_tensor(word_lengths):
    sns.set(style="whitegrid")
    
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(range(len(word_lengths))), y=word_lengths.numpy())
    
    plt.title("Word Lengths in the Text")
    plt.xlabel("Word Index")
    plt.ylabel("Word Length")
    plt.show()

def export_as_csv(pdf_path, csv_path):
    with open(csv_path, 'w', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file)
        for page_text in extract_text_by_page(pdf_path):
            processed_text = process_text(page_text)
            if processed_text:
                writer.writerow([processed_text])

def perform_full_process(pdf_path, csv_path):
    try:
        export_as_csv(pdf_path, csv_path)

       
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            text = csv_file.read()

     
        word_lengths = perform_tensor_operations(text)

        
        visualize_tensor(word_lengths)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == '__main__':
   
 
    
    perform_full_process(pdf_path, csv_path)
