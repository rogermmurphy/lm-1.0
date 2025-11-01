from async_presentation_tool import AsyncPresentationTool

tool = AsyncPresentationTool()
result = tool.create_presentation_async('Simple Math Test', n_slides=3)
print('Job created:', result['job_id'])
