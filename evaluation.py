import json
from typing import List, Dict, Any
from dataclasses import dataclass
import statistics
import json
import prompts
from RecatGPT import RecatGPT

@dataclass
class EvaluationResult:
    love_language: str
    prompt: str
    scores: Dict[str, float]
    feedback: str
    overall_score: float

# Test cases for different love languages
TEST_CASES = [
    {"love_language": "Words of Affirmation", "type": 1},
    {"love_language": "Quality Time", "type": 2},
    {"love_language": "Receiving Gifts", "type": 3},
    {"love_language": "Acts of Service", "type": 4},
    {"love_language": "Physical Touch", "type": 5},
]

def evaluate_prompt(love_language: str, prompt: str) -> EvaluationResult:
    """Evaluate a single prompt using the LLM judge."""
    judge_prompt = prompts.JUDGE_PROMPT.format(
        love_language=love_language,
        prompt=prompt
    )

    try:
        evaluation_response = RecatGPT.ask_gpt(judge_prompt, model="gpt-4o")
        
        # Parse JSON response
        eval_data = json.loads(evaluation_response)

        scores = {
            "love_language_alignment": eval_data["love_language_alignment"],
            "emotional_engagement": eval_data["emotional_engagement"],
            "specificity_depth": eval_data["specificity_depth"],
            "actionability": eval_data["actionability"],
            "app_context_fit": eval_data["app_context_fit"],
            "tone_appropriateness": eval_data["tone_appropriateness"]
        }
        
        overall_score = statistics.mean(scores.values())
        
        feedback = f"{eval_data['overall_feedback']}\n\nSuggestions: {eval_data['suggestions']}"
        
        return EvaluationResult(
            love_language=love_language,
            prompt=prompt,
            scores=scores,
            feedback=feedback,
            overall_score=overall_score
        )
        
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing evaluation response: {e}")
        return None

def run_evaluation_suite(num_samples: int = 3) -> List[EvaluationResult]:
    """Run evaluation on multiple samples for each love language."""
    all_results = []
    
    print("🔄 Running LLM Judge Evaluation Suite...")
    print("=" * 60)
    
    for test_case in TEST_CASES:
        print(f"\n📝 Evaluating: {test_case['love_language']}")
        print("-" * 40)
        
        for i in range(num_samples):
            # Generate prompt
            gpt_prompt = RecatGPT.get_love_language_prompt(test_case['type'])
            generated_prompt = RecatGPT.ask_gpt(gpt_prompt)
            
            print(f"\nSample {i+1}:")
            print(f"Generated Prompt: {generated_prompt}")
            
            # Evaluate prompt
            result = evaluate_prompt(test_case['love_language'], generated_prompt)
            
            if result:
                all_results.append(result)
                print(f"Overall Score: {result.overall_score:.2f}/10")
                print(f"Scores: {result.scores}")
                print(f"Feedback: {result.feedback[:200]}...")
            else:
                print("❌ Evaluation failed")
    
    return all_results

def generate_report(results: List[EvaluationResult]) -> None:
    """Generate a comprehensive evaluation report."""
    if not results:
        print("No results to report")
        return
    
    print("\n" + "="*80)
    print("📊 EVALUATION REPORT")
    print("="*80)
    
    # Overall statistics
    overall_scores = [r.overall_score for r in results]
    print(f"\n🎯 Overall Performance:")
    print(f"   Average Score: {statistics.mean(overall_scores):.2f}/10")
    print(f"   Best Score: {max(overall_scores):.2f}/10")
    print(f"   Worst Score: {min(overall_scores):.2f}/10")
    print(f"   Standard Deviation: {statistics.stdev(overall_scores):.2f}")
    
    # Performance by love language
    print(f"\n💝 Performance by Love Language:")
    for love_language in set(r.love_language for r in results):
        lang_results = [r for r in results if r.love_language == love_language]
        lang_scores = [r.overall_score for r in lang_results]
        print(f"   {love_language}: {statistics.mean(lang_scores):.2f}/10")
    
    # Performance by criteria
    print(f"\n📋 Performance by Criteria:")
    all_criteria = list(results[0].scores.keys())
    for criterion in all_criteria:
        criterion_scores = [r.scores[criterion] for r in results]
        print(f"   {criterion.replace('_', ' ').title()}: {statistics.mean(criterion_scores):.2f}/10")
    
    # Best and worst performing prompts
    best_result = max(results, key=lambda r: r.overall_score)
    worst_result = min(results, key=lambda r: r.overall_score)
    
    print(f"\n🏆 Best Performing Prompt ({best_result.overall_score:.2f}/10):")
    print(f"   Love Language: {best_result.love_language}")
    print(f"   Prompt: {best_result.prompt}")
    print(f"   Strengths: {best_result.feedback.split('Suggestions:')[0][:200]}...")
    
    print(f"\n⚠️  Lowest Performing Prompt ({worst_result.overall_score:.2f}/10):")
    print(f"   Love Language: {worst_result.love_language}")
    print(f"   Prompt: {worst_result.prompt}")
    print(f"   Areas for Improvement: {worst_result.feedback.split('Suggestions:')[1][:200] if 'Suggestions:' in worst_result.feedback else 'N/A'}...")

def save_results_to_file(results: List[EvaluationResult], filename: str = "evaluation_results.json") -> None:
    """Save evaluation results to a JSON file for further analysis."""
    results_data = []
    for result in results:
        results_data.append({
            "love_language": result.love_language,
            "prompt": result.prompt,
            "scores": result.scores,
            "overall_score": result.overall_score,
            "feedback": result.feedback
        })
    
    with open(filename, 'w') as f:
        json.dump(results_data, f, indent=2)
    
    print(f"\n💾 Results saved to {filename}")

def interactive_evaluation():
    """Interactive mode to test specific prompts."""
    print("\n🔍 Interactive Evaluation Mode")
    print("Enter a love language and prompt to get immediate feedback.")
    
    while True:
        love_language = input("\nEnter love language (or 'quit'): ")
        if love_language.lower() == 'quit':
            break
            
        prompt = input("Enter prompt to evaluate: ")
        
        result = evaluate_prompt(love_language, prompt)
        if result:
            print(f"\n📊 Evaluation Results:")
            print(f"Overall Score: {result.overall_score:.2f}/10")
            for criterion, score in result.scores.items():
                print(f"  {criterion.replace('_', ' ').title()}: {score}/10")
            print(f"\n💬 Feedback:\n{result.feedback}")

if __name__ == "__main__":
    print("🚀 ReCat Prompt Evaluation System")
    print("Choose an option:")
    print("1. Run full evaluation suite")
    print("2. Interactive evaluation")
    print("3. Quick test (1 sample per love language)")
    
    choice = input("\nEnter choice (1-3): ")
    
    if choice == "1":
        results = run_evaluation_suite(num_samples=3)
        generate_report(results)
        save_results_to_file(results)
        
    elif choice == "2":
        interactive_evaluation()
        
    elif choice == "3":
        results = run_evaluation_suite(num_samples=1)
        generate_report(results)
        save_results_to_file(results)
        
    else:
        print("Invalid choice")