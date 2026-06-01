/**
 * Google Apps Script for Meal Planner Sync
 * 
 * Instructions:
 * 1. Open your Google Sheet.
 * 2. Go to Extensions -> Apps Script.
 * 3. Delete any existing code and paste this script in.
 * 4. Click Save.
 * 5. Click Deploy -> New Deployment.
 * 6. Select "Web App" as the type.
 * 7. Set "Execute as" to "Me" (your email).
 * 8. Set "Who has access" to "Anyone" (this lets your web app send requests to it).
 * 9. Click Deploy and copy the Web App URL.
 * 10. Paste the Web App URL into your Meal Planner Settings!
 */

function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return ContentService.createTextOutput(JSON.stringify({ status: 'error', message: 'No post data received. Ensure you are sending a POST request with a valid body.' }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    const data = JSON.parse(e.postData.contents);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    if (!ss) {
      throw new Error("This script must be container-bound to a Google Sheet. Please open your Google Sheet, go to Extensions -> Apps Script, and paste this script there.");
    }
    
    if (data.action === 'logMeal') {
      const sheet = ss.getSheetByName('Meal Log') || ss.insertSheet('Meal Log');
      // Ensure headers if new sheet
      if (sheet.getLastRow() === 0) {
        sheet.appendRow(["Date cooked", "Week", "Day", "Meal", "Cuisine", "Cal/adult", "Est. cost", "Actual cost", "Rating (1-5)", "Favourite", "Notes"]);
      }
      
      const rows = sheet.getDataRange().getValues();
      let rowIndex = -1;
      
      // Look for existing row with same Week, Day, and Meal Name to update
      for (let i = 1; i < rows.length; i++) {
        if (rows[i][1] == data.week && rows[i][2] === data.day && rows[i][3] === data.meal) {
          rowIndex = i + 1; // 1-indexed
          break;
        }
      }
      
      if (rowIndex !== -1) {
        // Update existing row
        sheet.getRange(rowIndex, 1).setValue(data.dateCooked || new Date().toISOString().slice(0,10));
        sheet.getRange(rowIndex, 8).setValue(data.actualCost || "");
        sheet.getRange(rowIndex, 9).setValue(data.rating || "");
        sheet.getRange(rowIndex, 10).setValue(data.favourite ? "yes" : "");
        sheet.getRange(rowIndex, 11).setValue(data.notes || "");
      } else {
        // Append new row
        sheet.appendRow([
          data.dateCooked || new Date().toISOString().slice(0,10),
          data.week,
          data.day,
          data.meal,
          data.cuisine || "",
          data.calories || "",
          data.estCost || "",
          data.actualCost || "",
          data.rating || "",
          data.favourite ? "yes" : "",
          data.notes || ""
        ]);
      }
      
      return ContentService.createTextOutput(JSON.stringify({ status: 'success', message: 'Meal logged successfully' }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    if (data.action === 'syncAll') {
      const sheet = ss.getSheetByName('Meal Log') || ss.insertSheet('Meal Log');
      if (sheet.getLastRow() === 0) {
        sheet.appendRow(["Date cooked", "Week", "Day", "Meal", "Cuisine", "Cal/adult", "Est. cost", "Actual cost", "Rating (1-5)", "Favourite", "Notes"]);
      }
      
      const existingRows = sheet.getDataRange().getValues();
      
      data.meals.forEach(m => {
        let rowIndex = -1;
        for (let i = 1; i < existingRows.length; i++) {
          if (existingRows[i][1] == m.week && existingRows[i][2] === m.day && existingRows[i][3] === m.meal) {
            rowIndex = i + 1;
            break;
          }
        }
        
        if (rowIndex !== -1) {
          sheet.getRange(rowIndex, 1).setValue(m.dateCooked || existingRows[rowIndex-1][0] || new Date().toISOString().slice(0,10));
          sheet.getRange(rowIndex, 8).setValue(m.actualCost || existingRows[rowIndex-1][7] || "");
          sheet.getRange(rowIndex, 9).setValue(m.rating || "");
          sheet.getRange(rowIndex, 10).setValue(m.favourite ? "yes" : "");
          sheet.getRange(rowIndex, 11).setValue(m.notes || "");
        } else {
          sheet.appendRow([
            m.dateCooked || new Date().toISOString().slice(0,10),
            m.week,
            m.day,
            m.meal,
            m.cuisine || "",
            m.calories || "",
            m.estCost || "",
            m.actualCost || "",
            m.rating || "",
            m.favourite ? "yes" : "",
            m.notes || ""
          ]);
        }
      });
      
      return ContentService.createTextOutput(JSON.stringify({ status: 'success', message: 'All meals synced' }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    return ContentService.createTextOutput(JSON.stringify({ status: 'error', message: 'Unknown action' }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ status: 'error', message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Add simple GET test endpoint
function doGet(e) {
  return ContentService.createTextOutput("Google Sheets Sync Endpoint is ACTIVE. Use POST method to sync data.")
    .setMimeType(ContentService.MimeType.TEXT);
}
