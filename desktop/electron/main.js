# SignBridge Desktop App - Electron
# Cross-platform desktop application for Windows, macOS, and Linux

const { app, BrowserWindow, Menu, ipcMain, dialog, shell } = require('electron');
const path = require('path');
const fs = require('fs');

class SignBridgeDesktop {
  constructor() {
    this.mainWindow = null;
    this.isQuitting = false;
    
    // Initialize the application
    this.initializeApp();
  }

  initializeApp() {
    // Handle app ready
    app.whenReady().then(() => {
      this.createMainWindow();
      this.createMenu();
      this.setupIPC();
      
      app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
          this.createMainWindow();
        }
      });
    });

    // Handle window closed
    app.on('window-all-closed', () => {
      if (process.platform !== 'darwin') {
        app.quit();
      }
    });

    // Handle before quit
    app.on('before-quit', () => {
      this.isQuitting = true;
    });
  }

  createMainWindow() {
    // Create the browser window
    this.mainWindow = new BrowserWindow({
      width: 1200,
      height: 800,
      minWidth: 800,
      minHeight: 600,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
        enableRemoteModule: true
      },
      icon: path.join(__dirname, 'assets', 'icon.png'),
      titleBarStyle: 'default',
      show: false
    });

    // Load the HTML file
    this.mainWindow.loadFile(path.join(__dirname, 'index.html'));

    // Show window when ready
    this.mainWindow.once('ready-to-show', () => {
      this.mainWindow.show();
      
      // Focus on Windows
      if (process.platform === 'win32') {
        this.mainWindow.focus();
      }
    });

    // Handle window closed
    this.mainWindow.on('closed', () => {
      this.mainWindow = null;
    });

    // Handle minimize to tray (optional)
    this.mainWindow.on('minimize', () => {
      if (process.platform === 'win32') {
        this.mainWindow.hide();
      }
    });

    // Open external links in default browser
    this.mainWindow.webContents.setWindowOpenHandler(({ url }) => {
      shell.openExternal(url);
      return { action: 'deny' };
    });
  }

  createMenu() {
    const template = [
      {
        label: 'File',
        submenu: [
          {
            label: 'New Conversation',
            accelerator: 'CmdOrCtrl+N',
            click: () => {
              this.mainWindow.webContents.send('menu-new-conversation');
            }
          },
          {
            label: 'Open Conversation',
            accelerator: 'CmdOrCtrl+O',
            click: async () => {
              const result = await dialog.showOpenDialog(this.mainWindow, {
                properties: ['openFile'],
                filters: [
                  { name: 'JSON Files', extensions: ['json'] },
                  { name: 'All Files', extensions: ['*'] }
                ]
              });
              
              if (!result.canceled) {
                this.mainWindow.webContents.send('menu-open-conversation', result.filePaths[0]);
              }
            }
          },
          {
            label: 'Save Conversation',
            accelerator: 'CmdOrCtrl+S',
            click: () => {
              this.mainWindow.webContents.send('menu-save-conversation');
            }
          },
          { type: 'separator' },
          {
            label: 'Exit',
            accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
            click: () => {
              app.quit();
            }
          }
        ]
      },
      {
        label: 'Edit',
        submenu: [
          { role: 'undo' },
          { role: 'redo' },
          { type: 'separator' },
          { role: 'cut' },
          { role: 'copy' },
          { role: 'paste' },
          { role: 'selectall' }
        ]
      },
      {
        label: 'View',
        submenu: [
          {
            label: 'Toggle Fullscreen',
            accelerator: 'F11',
            click: () => {
              this.mainWindow.setFullScreen(!this.mainWindow.isFullScreen());
            }
          },
          {
            label: 'Toggle Developer Tools',
            accelerator: process.platform === 'darwin' ? 'Alt+Cmd+I' : 'Ctrl+Shift+I',
            click: () => {
              this.mainWindow.webContents.toggleDevTools();
            }
          },
          { type: 'separator' },
          { role: 'reload' },
          { role: 'forceReload' },
          { role: 'toggleDevTools' },
          { type: 'separator' },
          { role: 'resetZoom' },
          { role: 'zoomIn' },
          { role: 'zoomOut' },
          { type: 'separator' },
          { role: 'togglefullscreen' }
        ]
      },
      {
        label: 'SignBridge',
        submenu: [
          {
            label: 'About SignBridge',
            click: () => {
              dialog.showMessageBox(this.mainWindow, {
                type: 'info',
                title: 'About SignBridge',
                message: 'SignBridge Desktop',
                detail: 'AI-Enhanced Communication Assistant\nVersion 1.0.0\n\nPowered by TensorFlow and OpenCV'
              });
            }
          },
          {
            label: 'Sign Dictionary',
            click: () => {
              this.mainWindow.webContents.send('menu-show-signs');
            }
          },
          {
            label: 'Statistics',
            click: () => {
              this.mainWindow.webContents.send('menu-show-stats');
            }
          },
          { type: 'separator' },
          {
            label: 'Preferences',
            accelerator: 'CmdOrCtrl+,',
            click: () => {
              this.mainWindow.webContents.send('menu-show-preferences');
            }
          }
        ]
      },
      {
        label: 'Help',
        submenu: [
          {
            label: 'User Guide',
            click: () => {
              shell.openExternal('https://github.com/invecta/signbridge-app');
            }
          },
          {
            label: 'Keyboard Shortcuts',
            click: () => {
              this.mainWindow.webContents.send('menu-show-shortcuts');
            }
          },
          { type: 'separator' },
          {
            label: 'Report Issue',
            click: () => {
              shell.openExternal('https://github.com/invecta/signbridge-app/issues');
            }
          }
        ]
      }
    ];

    // macOS specific menu adjustments
    if (process.platform === 'darwin') {
      template.unshift({
        label: app.getName(),
        submenu: [
          { role: 'about' },
          { type: 'separator' },
          { role: 'services' },
          { type: 'separator' },
          { role: 'hide' },
          { role: 'hideothers' },
          { role: 'unhide' },
          { type: 'separator' },
          { role: 'quit' }
        ]
      });
    }

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
  }

  setupIPC() {
    // Handle camera permission request
    ipcMain.handle('request-camera-permission', async () => {
      try {
        // In a real implementation, you would request camera permission
        // For now, we'll simulate success
        return { success: true, permission: 'granted' };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    // Handle sign recognition
    ipcMain.handle('recognize-sign', async (event, imageData) => {
      try {
        // In a real implementation, this would call the AI model
        // For now, we'll simulate recognition
        const mockSigns = [
          { name: 'hello', description: 'Wave hand in greeting motion', confidence: 0.9 },
          { name: 'yes', description: 'Make fist and nod up and down', confidence: 0.9 },
          { name: 'no', description: 'Index finger shakes side to side', confidence: 0.85 },
          { name: 'thank_you', description: 'Flat hand touches chin and moves forward', confidence: 0.85 },
          { name: 'please', description: 'Flat hand circles on chest', confidence: 0.85 }
        ];
        
        const randomSign = mockSigns[Math.floor(Math.random() * mockSigns.length)];
        
        return {
          success: true,
          result: {
            sign: randomSign.name,
            confidence: randomSign.confidence,
            description: randomSign.description,
            ai_enabled: true
          }
        };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    // Handle conversation save
    ipcMain.handle('save-conversation', async (event, conversationData) => {
      try {
        const result = await dialog.showSaveDialog(this.mainWindow, {
          defaultPath: signbridge_conversation_.json,
          filters: [
            { name: 'JSON Files', extensions: ['json'] },
            { name: 'All Files', extensions: ['*'] }
          ]
        });
        
        if (!result.canceled) {
          fs.writeFileSync(result.filePath, JSON.stringify(conversationData, null, 2));
          return { success: true, filePath: result.filePath };
        } else {
          return { success: false, error: 'Save cancelled' };
        }
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    // Handle conversation load
    ipcMain.handle('load-conversation', async (event, filePath) => {
      try {
        const data = fs.readFileSync(filePath, 'utf8');
        const conversation = JSON.parse(data);
        return { success: true, conversation };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    // Handle app info
    ipcMain.handle('get-app-info', () => {
      return {
        name: app.getName(),
        version: app.getVersion(),
        platform: process.platform,
        arch: process.arch
      };
    });
  }
}

// Create the application instance
const signBridgeApp = new SignBridgeDesktop();

// Export for testing
module.exports = SignBridgeDesktop;
