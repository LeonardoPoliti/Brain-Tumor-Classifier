## **Brain Tumor Classification** 
**A Comparative Analysis of Image-Based and Texture-Based Approaches**

Brain tumor classification is a critical task in medical image analysis, with significant implications for diagnosis, treatment planning, and patient prognosis. Early and accurate identification of tumor type is crucial for guiding therapeutic interventions and improving patient outcomes. Magnetic Resonance Imaging (MRI) has emerged as a valuable tool for non-invasive brain tumor assessment, providing detailed anatomical information and enabling the visualization of tumor characteristics. In recent years, improvements in machine learning and deep learning techniques have revolutionised the field of medical image analysis, offering the potential for automated, objective and accurate tumour classification.

**AIM:** This project examines the effectiveness of texture features derived from Gray Level Co-occurrence Matrices (GLCM) in distinguishing healthy brain tissue from three distinct tumor types: Glioma, Meningioma, and Pituitary tumors. A soft-voting ensemble model, combining the predictive power of a Support Vector Classifier (SVC), a Random Forest (RF), and a Multi-Layer Perceptron (MLP), trained on extracted texture features, is evaluated against the performance of more complex Convolutional Neural Networks (CNNs), obtained through custom architecture design or transfer learning (VGG19), which directly analyze MRI images for brain tumor classification.

**DATA:** The dataset consists of approximately 7000 images obtained from magnetic resonance imaging (MRI) of healthy patients and patients with three different types of brain tumours: Glioma, Meningioma and Pituitary tumour. The data was obtained from Kaggle and was slightly modified to remove the pre-made train-test split. (https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset/data)

**Drive project folder:**  https://drive.google.com/drive/folders/1Chuf9lPrYOU7MyEWxG14X5aPbLZa4y_c?usp=sharing
