# Automating Invoice Reporting with UiPath Web Studio

Jason Teixeira · TripleTen AI Automation

## Contents

- **Presentation/**: original eight-slide deck and revised 14-slide deck with the four requested configuration views, the empty Else branch, and a Document Understanding warning review.
- **Workflow/**: UiPath Studio Web solution export and Main.xaml.
- **Evidence/**: screenshots from the successful test run and full-screen UiPath configuration captures.
- **Sample-Invoices/**: all six supplied PDF invoices.

## Live links

- [Google Slides presentation](https://docs.google.com/presentation/d/1qOMtMsHBpJHjYEha4O_VBPXVe0JN2G0ESTgIWDukNDQ/edit)
- [Google Sheet report](https://docs.google.com/spreadsheets/d/1rUDw-2mJnMi5nBwOikze-hPChpt_7e-k_3MpVrM8wVU/edit)
- [UiPath workflow](https://cloud.uipath.com/sageideasllc/studio_/designer/d9b96923-0a75-4b56-9910-65b2947083f0?solutionId=7d9a4655-6550-4d5b-8ee9-08df3048409f)
- [Google Drive project folder](https://drive.google.com/drive/folders/16fhX_YrWZJb60o3myeo7fmAWlRtWdDfj)

The successful test processed six invoices, produced four populated report rows and logged a low-confidence invoice-number warning. The log does not identify the source filename. Rerunning the workflow appends duplicate rows. The live presentation is viewable by anyone with the link.

Use **Presentation/Invoice-Reporting-Presentation-Revised.pptx** for resubmission. It includes screenshots of the confidence If and Warn branch, the complete due date expression, the 15-word system prompt, all five Write Row mappings, and the Document Understanding banner. The warning indicates that the predefined model is outside the solution definitions for deployment to another tenant; the local run succeeded.
