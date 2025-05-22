import os
import json
from openai import OpenAI
from slither import Slither
from slither.core.declarations.function import Function

class ThothAnalyzer:
    def __init__(self, contract_path):
        self.contract_path = contract_path
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.findings = []

    def analyze(self):
        self._static_analysis()
        self._llm_analysis()
        return self.findings

    def _static_analysis(self):
        """Dynamic analysis of all state-changing functions"""
        try:
            slither = Slither(self.contract_path)
        
            for contract in slither.contracts:
                for func in contract.functions:
                    if self._is_state_changing(func) and self._is_externally_callable(func):
                        if not self._has_proper_access_control(func):
                            self.findings.append({
                                'severity': 'HIGH',
                                'description': f'Missing access control on {func.name}',
                                'recommendation': self._generate_recommendation(func),
                                'source': 'Static Analysis'
                            })
        except Exception as e:
            print(f"Static analysis error: {str(e)}")

    def _is_state_changing(self, func) -> bool:
        """Check if function modifies contract state"""
        return not (func.view or func.pure)

    def _is_externally_callable(self, func) -> bool:
        """Check if function can be called externally"""
        return func.visibility in ['public', 'external']


    def _has_proper_access_control(self, func: Function) -> bool:
        """Check for access control patterns using multiple heuristics"""
        # Check modifiers
        common_acl_modifiers = {'onlyOwner', 'onlyRole', 'authenticated', 'whenNotPaused'}
        if any(m.name in common_acl_modifiers for m in func.modifiers):
            return True
            
        # Check function logic for common access control patterns
        if any(n for n in func.nodes if 'require(' in str(n) and ('msg.sender' in str(n) or 'owner' in str(n))):
            return True
            
        # Check inheritance from known access control contracts
        inherited_contracts = [c.name for c in func.contract.inheritance]
        if any(name in ['Ownable', 'AccessControl'] for name in inherited_contracts):
            return True
            
        return False

    def _generate_recommendation(self, func: Function) -> str:
        """Generate context-aware recommendations"""
        inherited_contracts = [c.name for c in func.contract.inheritance]
        
        if 'Ownable' in inherited_contracts:
            return f"Add onlyOwner modifier to {func.name}"
        elif 'AccessControl' in inherited_contracts:
            return f"Add role-based restriction using onlyRole modifier to {func.name}"
        else:
            return ("Implement access control using:\n"
                    "1. OpenZeppelin Ownable for simple ownership\n"
                    "2. OpenZeppelin AccessControl for role-based permissions\n"
                    "3. Custom modifier with require(msg.sender == authorizedAddress)")

    def _llm_analysis(self):
        """LLM-powered contextual vulnerability detection"""
        try:
            with open(self.contract_path, 'r') as f:
                code = f.read()

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": f"""Analyze this Solidity contract and identify vulnerabilities. 
                    Focus on access control issues. Return findings in JSON format:
                    {{
                        "findings": [
                            {{
                                "function": "function_name",
                                "vulnerability": "vulnerability_type",
                                "description": "detailed_explanation",
                                "recommendation": "mitigation_step"
                            }}
                        ]
                    }}
                    
                    Contract code:
                    {code}"""
                }],
                temperature=0.1,
                response_format={"type": "json_object"}
            )

            llm_response = json.loads(response.choices[0].message.content)
            for finding in llm_response.get('findings', []):
                self.findings.append({
                    'severity': 'MEDIUM', 
                    'description': f"{finding['vulnerability']} in {finding['function']}",
                    'recommendation': finding['recommendation'],
                    'source': 'LLM Analysis'
                })

        except json.JSONDecodeError:
            print("Failed to parse LLM response as JSON")
        except Exception as e:
            print(f"LLM analysis error: {str(e)}")

if __name__ == "__main__":
    analyzer = ThothAnalyzer("KiloPriceFeed.sol")
    results = analyzer.analyze()
    
    print("Thoth Analysis Results:")
    for finding in results:
        print(f"[{finding['severity']}] {finding['description']}")
        print(f"Recommendation: {finding['recommendation']}\n")
