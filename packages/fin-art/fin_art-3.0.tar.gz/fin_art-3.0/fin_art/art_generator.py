import warnings
# Отключаем предупреждения
warnings.filterwarnings("ignore")

# Отключаем логи для библиотеки transformers
from transformers import logging as transformers_logging
transformers_logging.set_verbosity_error()

# Отключаем логи для библиотеки diffusers
from diffusers import logging as diffusers_logging
diffusers_logging.set_verbosity_error()

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from diffusers import StableDiffusionPipeline
import matplotlib.pyplot as plt

class ImageGenerator:
    LORA_PATHS = {
        "pixel": "madvasik/pixel-art-lora",
        "ink": "madvasik/ink-art-lora",
        "cyberpunk": "madvasik/cyberpunk-lora",
        "lego": "madvasik/lego-lora",
        "glasssculpture": "madvasik/glasssculpture-lora"
    }

    # базовый негатив промпт
    base_negative = "low quality, low res, blurry, distortion, cropped, jpeg artifacts, duplicate, ugly, bad anatomy, bad proportions, deformed, malformed, off-screen, low resolution, unattractive, unnatural pose"

    # базовые промпты для лор
    base_lora_prompts = {
        "pixel": "pixel, ",
        "ink": "white background, scenery, ink, ",
        "cyberpunk": "CyberpunkAI, ",
        "lego": "LEGO Creator, ",
        "glasssculpture": "glasssculpture, transparent, translucent, reflections, "
    }

    def __init__(self, model_name='k1tub/gpt2_prompts',
                 tokenizer_name='distilbert/distilgpt2',
                 stable_diff_model='stable-diffusion-v1-5/stable-diffusion-v1-5',
                 lora_type='pixel',
                 device='cuda'):
        self.device = device

        if lora_type is not None and lora_type not in self.LORA_PATHS:
            raise ValueError(f"Invalid LoRA type: {lora_type}. Choose from {list(self.LORA_PATHS.keys())} or None to skip.")
        

        # GPT и токенизатор
        self.tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token  # Устанавливаем pad_token как eos_token
        self.model = GPT2LMHeadModel.from_pretrained(model_name).to(device)

        # пайплайн Stable Diffusion 
        self.text2img_pipe = StableDiffusionPipeline.from_pretrained(
            stable_diff_model, torch_dtype=torch.float16, 
            safety_checker = None, requires_safety_checker = False).to(device)

        # Загружаем LoRA
        if lora_type is not None:
            self.load_lora_weights(lora_type)
            # триггер слова для лоры
            self.base_prompt = self.base_lora_prompts[lora_type]
        else:
          self.base_prompt = ''

    def load_lora_weights(self, lora_type):
        """Загружает LoRA веса на основе выбранного типа."""
        lora_path = self.LORA_PATHS[lora_type]
        print(f"Loading LoRA weights: {lora_path}")
        self.text2img_pipe.load_lora_weights(lora_path)

    def improve_with_gpt(self, input_prompt):
        """Улучшает входной промт с помощью GPT-2."""
        input_ids = self.tokenizer.encode(input_prompt, return_tensors="pt").to(self.device)
        attention_mask = torch.ones(input_ids.shape, device=self.device)
        out = self.model.generate(
            input_ids, attention_mask=attention_mask,
            max_length=70, num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id
        )
        improved_prompt = self.tokenizer.decode(out[0], skip_special_tokens=True)
        return improved_prompt

    def generate_images(self, input_prompt, num_images=1, num_inference_steps=50,
                        show_prompt=False, improve_prompt=False, negative_prompt=base_negative):
        """Генерирует изображения на основе текста, с возможным улучшением промта."""
        
        # Улучшаем промпт (если improve_prompt=True)
        if improve_prompt:
            input_prompt = self.improve_with_gpt(input_prompt)

        prompts = [input_prompt] * num_images

        # Генерация изображений
        images = []
        for prompt in prompts:
            image = self.text2img_pipe(self.base_prompt + prompt, num_inference_steps=num_inference_steps, negative_prompt=negative_prompt).images[0]
            images.append((image, prompt))

        for img, prompt in images:
            if show_prompt:
                print(f"Generated prompt: {self.base_prompt + prompt}")
            plt.figure(figsize=(6, 6))
            plt.imshow(img)
            plt.axis("off")
            plt.show()
