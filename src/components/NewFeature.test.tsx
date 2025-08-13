import { render, screen } from '@testing-library/react';
import NewFeature from './NewFeature';

describe('NewFeature', () => {
  it('renders correctly', () => {
    render(<NewFeature />);
    expect(screen.getByText('New Feature')).toBeInTheDocument();
  });
});