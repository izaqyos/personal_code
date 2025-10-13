import React, { useEffect, useState } from 'react';
import { Settings, X, Loader2 } from 'lucide-react';
import { APISettings, OllamaModel } from '../types';
import { fetchOllamaModels } from '../services/llm';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  settings: APISettings;
  onSave: (settings: APISettings) => void;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({
  isOpen,
  onClose,
  settings,
  onSave,
}) => {
  const [localSettings, setLocalSettings] = React.useState<APISettings>(settings);
  const [ollamaModels, setOllamaModels] = useState<OllamaModel[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen && localSettings.ollamaUrl) {
      loadOllamaModels();
    }
  }, [isOpen, localSettings.ollamaUrl]);

  const loadOllamaModels = async () => {
    try {
      setLoading(true);
      setError(null);
      const models = await fetchOllamaModels(localSettings.ollamaUrl);
      setOllamaModels(models);
      
      // Set default model if none selected
      if (!localSettings.ollamaModel && models.length > 0) {
        handleChange('ollamaModel', models[0].name);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch models');
      setOllamaModels([]);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(localSettings);
    onClose();
  };

  const handleChange = (key: keyof APISettings, value: string) => {
    setLocalSettings(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-lg p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <Settings className="w-5 h-5" />
            <h2 className="text-xl font-semibold">API Settings</h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              OpenAI API Key
            </label>
            <input
              type="password"
              value={localSettings.openai}
              onChange={(e) => handleChange('openai', e.target.value)}
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:border-blue-500"
              placeholder="sk-..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Anthropic API Key
            </label>
            <input
              type="password"
              value={localSettings.anthropic}
              onChange={(e) => handleChange('anthropic', e.target.value)}
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:border-blue-500"
              placeholder="sk-ant-..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Google API Key (Gemini)
            </label>
            <input
              type="password"
              value={localSettings.gemini}
              onChange={(e) => handleChange('gemini', e.target.value)}
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:border-blue-500"
              placeholder="AIza..."
            />
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Ollama URL
            </label>
            <input
              type="text"
              value={localSettings.ollamaUrl}
              onChange={(e) => handleChange('ollamaUrl', e.target.value)}
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:border-blue-500"
              placeholder="http://localhost:11434"
            />
            
            <div className="flex items-center gap-2">
              <label className="block text-sm font-medium text-gray-700">
                Ollama Model
              </label>
              <button
                type="button"
                onClick={loadOllamaModels}
                className="text-sm text-blue-500 hover:text-blue-600"
              >
                Refresh
              </button>
            </div>
            
            {loading ? (
              <div className="flex items-center gap-2 text-gray-500">
                <Loader2 className="w-4 h-4 animate-spin" />
                Loading models...
              </div>
            ) : error ? (
              <div className="text-red-500 text-sm">{error}</div>
            ) : (
              <select
                value={localSettings.ollamaModel}
                onChange={(e) => handleChange('ollamaModel', e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:border-blue-500"
              >
                {ollamaModels.length === 0 ? (
                  <option value="">No models available</option>
                ) : (
                  ollamaModels.map((model) => (
                    <option key={model.name} value={model.name}>
                      {model.name}
                    </option>
                  ))
                )}
              </select>
            )}
          </div>

          <div className="flex justify-end gap-2 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 hover:text-gray-900"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              Save Settings
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};