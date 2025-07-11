"""
Calculate Mean Operation

Modular operation for calculating statistical mean with comprehensive error handling.
"""

import logging
from typing import Dict, Any, List, Union, Optional
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CalculateMeanOperation:
    """Calculate statistical mean with comprehensive error handling and validation."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the calculate mean operation.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
    def calculate_mean(self, data: List[Union[int, float]], 
                      mean_type: str = 'arithmetic') -> Dict[str, Any]:
        """Calculate the mean of a dataset with comprehensive error handling.
        
        Args:
            data: List of numerical values
            mean_type: Type of mean to calculate ('arithmetic', 'geometric', 'harmonic')
            
        Returns:
            Dictionary containing calculation result
        """
        try:
            # Validate input data
            if not data:
                logger.error("Data list cannot be empty")
                return {
                    'success': False,
                    'error': 'Data list cannot be empty',
                    'operation': 'calculate_mean'
                }
            
            if not isinstance(data, list):
                logger.error(f"Data must be a list, got {type(data)}")
                return {
                    'success': False,
                    'error': f'Data must be a list, got {type(data)}',
                    'operation': 'calculate_mean'
                }
            
            # Validate data types
            valid_numbers = []
            invalid_values = []
            
            for i, value in enumerate(data):
                if isinstance(value, (int, float)):
                    if not (isinstance(value, bool)):  # Exclude boolean values
                        valid_numbers.append(float(value))
                    else:
                        invalid_values.append((i, value, 'boolean_not_allowed'))
                else:
                    invalid_values.append((i, value, 'not_numeric'))
            
            if not valid_numbers:
                logger.error("No valid numeric values found in data")
                return {
                    'success': False,
                    'error': 'No valid numeric values found in data',
                    'invalid_values': invalid_values,
                    'operation': 'calculate_mean'
                }
            
            # Validate mean type
            valid_types = ['arithmetic', 'geometric', 'harmonic']
            if mean_type not in valid_types:
                logger.warning(f"Invalid mean_type '{mean_type}', using 'arithmetic'")
                mean_type = 'arithmetic'
            
            # Calculate the mean based on type
            if mean_type == 'arithmetic':
                mean_value = statistics.mean(valid_numbers)
            elif mean_type == 'geometric':
                # Check for non-positive values
                if any(x <= 0 for x in valid_numbers):
                    logger.error("Geometric mean requires all values to be positive")
                    return {
                        'success': False,
                        'error': 'Geometric mean requires all values to be positive',
                        'operation': 'calculate_mean'
                    }
                mean_value = statistics.geometric_mean(valid_numbers)
            else:  # harmonic
                # Check for zero values
                if any(x == 0 for x in valid_numbers):
                    logger.error("Harmonic mean requires all values to be non-zero")
                    return {
                        'success': False,
                        'error': 'Harmonic mean requires all values to be non-zero',
                        'operation': 'calculate_mean'
                    }
                mean_value = statistics.harmonic_mean(valid_numbers)
            
            # Calculate additional statistics
            data_length = len(valid_numbers)
            min_value = min(valid_numbers)
            max_value = max(valid_numbers)
            range_value = max_value - min_value
            
            # Calculate variance and standard deviation
            try:
                variance = statistics.variance(valid_numbers)
                std_dev = statistics.stdev(valid_numbers)
            except statistics.StatisticsError:
                variance = None
                std_dev = None
            
            # Prepare result
            result = {
                'success': True,
                'mean': mean_value,
                'mean_type': mean_type,
                'data_length': data_length,
                'min_value': min_value,
                'max_value': max_value,
                'range': range_value,
                'operation': 'calculate_mean'
            }
            
            # Add variance and standard deviation if available
            if variance is not None:
                result['variance'] = variance
            if std_dev is not None:
                result['standard_deviation'] = std_dev
            
            # Add information about invalid values if any
            if invalid_values:
                result['invalid_values_count'] = len(invalid_values)
                result['invalid_values'] = invalid_values[:10]  # Limit to first 10 for readability
            
            # Add data summary
            result['data_summary'] = {
                'total_values': len(data),
                'valid_values': data_length,
                'data_type': 'numeric',
                'precision': self._determine_precision(valid_numbers)
            }
            
            logger.info(f"Successfully calculated {mean_type} mean: {mean_value}")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating mean: {e}")
            return {
                'success': False,
                'error': f'Error calculating mean: {str(e)}',
                'operation': 'calculate_mean'
            }
    
    def _determine_precision(self, numbers: List[float]) -> str:
        """Determine the precision of the numeric data."""
        # Check if all numbers are integers
        if all(x.is_integer() for x in numbers):
            return 'integer'
        
        # Check decimal places
        max_decimals = 0
        for num in numbers:
            if not num.is_integer():
                decimal_str = str(num).split('.')[-1]
                max_decimals = max(max_decimals, len(decimal_str))
        
        if max_decimals <= 2:
            return 'low_precision'
        elif max_decimals <= 6:
            return 'medium_precision'
        else:
            return 'high_precision'

def calculate_mean(data: List[Union[int, float]], 
                  mean_type: str = 'arithmetic') -> Dict[str, Any]:
    """Convenience function for calculating the mean of a dataset.
    
    Args:
        data: List of numerical values
        mean_type: Type of mean to calculate ('arithmetic', 'geometric', 'harmonic')
        
    Returns:
        Dictionary containing calculation result
    """
    operation = CalculateMeanOperation()
    return operation.calculate_mean(data, mean_type) 