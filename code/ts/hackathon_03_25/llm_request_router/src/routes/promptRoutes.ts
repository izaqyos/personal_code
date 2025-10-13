import express from 'express';
import { 
  createAnthropicClient, 
  getSystemPrompt, 
  getModelConfig,
  getRequestType,
  getActionType
} from '../utils/llmUtils';

// Define types
interface UserPromptRequest {
  text: string;
}

interface UserPromptResponse {
  response: string;
  requestType?: string;
  actionType?: string;
  error?: string;
}

const router = express.Router();

/**
 * @swagger
 * /api/get_user_prompt:
 *   post:
 *     summary: Get a response from the Content Design Time Assistant
 *     description: Sends a text prompt to the assistant and receives a classified response
 *     tags:
 *       - Assistant API
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/UserPromptRequest'
 *     responses:
 *       200:
 *         description: Successful response
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/UserPromptResponse'
 *       400:
 *         description: Bad request - text field is missing
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/UserPromptResponse'
 *       500:
 *         description: Server error
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/UserPromptResponse'
 */
// POST endpoint to handle user prompts
router.post('/get_user_prompt', function(req, res) {
  (async () => {
    try {
      console.log('Received request with body:', req.body);
      
      const requestBody = req.body as UserPromptRequest;
      const text = requestBody.text;
      
      if (!text) {
        return res.status(400).json({ 
          response: '',
          error: 'Text field is required in the request body' 
        } as UserPromptResponse);
      }

      try {
        // Create Anthropic client
        const anthropic = createAnthropicClient();
        
        // Get the appropriate system prompt based on the request
        const systemPrompt = await getSystemPrompt(text);
        
        // Get request classification
        const requestType = await getRequestType(text);
        const actionType = requestType === 'action' ? getActionType(text) : null;
        
        console.log(`Request classified as: ${requestType}${actionType ? `, Action: ${actionType}` : ''}`);
        console.log('Using system prompt type:', systemPrompt.substring(0, 50) + '...');
        
        // Get model configuration
        const modelConfig = getModelConfig();
        
        // Call Anthropic API with the latest structure and system prompt
        const message = await anthropic.messages.create({
          model: modelConfig.model,
          max_tokens: modelConfig.max_tokens,
          temperature: modelConfig.temperature,
          system: systemPrompt,
          messages: [
            { role: 'user', content: text }
          ]
        });

        // Extract the response text from the content block
        const responseText = message.content[0].type === 'text' 
          ? message.content[0].text 
          : 'Unable to process the response';

        console.log('Received response from Anthropic API');
        
        return res.status(200).json({ 
          response: responseText,
          requestType,
          actionType: actionType || undefined
        } as UserPromptResponse);
      } catch (apiError) {
        console.error('Error calling Anthropic API:', apiError);
        return res.status(500).json({ 
          response: '',
          error: `Error calling Anthropic API: ${apiError instanceof Error ? apiError.message : String(apiError)}` 
        } as UserPromptResponse);
      }
      
    } catch (error) {
      console.error('Error processing request:', error);
      return res.status(500).json({ 
        response: '',
        error: 'An error occurred while processing your request' 
      } as UserPromptResponse);
    }
  })();
});

export default router; 