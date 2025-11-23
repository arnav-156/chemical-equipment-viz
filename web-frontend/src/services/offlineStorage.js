// IndexedDB wrapper for offline data storage

class OfflineStorage {
  constructor() {
    this.dbName = 'ChemVizOfflineDB';
    this.version = 1;
    this.db = null;
  }

  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve(this.db);
      };

      request.onupgradeneeded = (event) => {
        const db = event.target.result;

        if (!db.objectStoreNames.contains('datasets')) {
          const datasetsStore = db.createObjectStore('datasets', { 
            keyPath: 'id', 
            autoIncrement: true 
          });
          datasetsStore.createIndex('timestamp', 'timestamp', { unique: false });
          datasetsStore.createIndex('synced', 'synced', { unique: false });
        }

        if (!db.objectStoreNames.contains('equipmentData')) {
          const equipmentStore = db.createObjectStore('equipmentData', { 
            keyPath: 'id', 
            autoIncrement: true 
          });
          equipmentStore.createIndex('datasetId', 'datasetId', { unique: false });
        }
      };
    });
  }

  async saveDataset(dataset) {
    if (!this.db) await this.init();

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['datasets'], 'readwrite');
      const store = transaction.objectStore('datasets');
      
      const datasetWithMeta = {
        ...dataset,
        timestamp: Date.now(),
        synced: false,
        offline: true
      };

      const request = store.add(datasetWithMeta);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async getDatasets() {
    if (!this.db) await this.init();

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['datasets'], 'readonly');
      const store = transaction.objectStore('datasets');
      const request = store.getAll();
      
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async getUnsyncedData() {
    if (!this.db) await this.init();

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['datasets'], 'readonly');
      const store = transaction.objectStore('datasets');
      const index = store.index('synced');
      const request = index.getAll(false);
      
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async markAsSynced(id) {
    if (!this.db) await this.init();

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['datasets'], 'readwrite');
      const store = transaction.objectStore('datasets');
      
      const getRequest = store.get(id);
      getRequest.onsuccess = () => {
        const data = getRequest.result;
        if (data) {
          data.synced = true;
          const putRequest = store.put(data);
          putRequest.onsuccess = () => resolve(putRequest.result);
          putRequest.onerror = () => reject(putRequest.error);
        } else {
          reject(new Error('Data not found'));
        }
      };
      getRequest.onerror = () => reject(getRequest.error);
    });
  }
}

export default new OfflineStorage();
