# KMI bot

LINE bot that imitates my friend. (This is joke bot)

`./model` includes the fine-tuned model I created from my friend's chat texts and [Japanese GPT-2 pretrained model](https://huggingface.co/rinna/japanese-gpt2-small).
This bot just generates the text from the given word with the model.

## Development

This is running on AWS API Gateway + Docker Lambda. After running `docker build .`, It needs publishing to private ECR.
