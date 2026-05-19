import React, { useEffect, useRef } from 'react';
import styled from 'styled-components';
import { srConfig } from '@config';
import sr from '@utils/sr';
import { Icon } from '@components/icons';
import { usePrefersReducedMotion } from '@hooks';

const StyledPublicationsSection = styled.section`
  max-width: 700px;
`;

const StyledPublicationsList = styled.ul`
  ${({ theme }) => theme.mixins.resetList};
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const StyledPublication = styled.li`
  position: relative;
  padding: 25px;
  border-radius: var(--border-radius);
  background-color: var(--light-navy);
  transition: var(--transition);

  &:hover {
    transform: translateY(-3px);
  }

  .pub-title {
    margin: 0 0 6px;
    color: var(--lightest-slate);
    font-size: var(--fz-xl);
    font-weight: 600;
    line-height: 1.3;
  }

  .pub-venue {
    margin: 0 0 14px;
    color: var(--slate);
    font-family: var(--font-mono);
    font-size: var(--fz-xs);
    font-style: italic;
  }

  .pub-description {
    color: var(--light-slate);
    font-size: var(--fz-md);
    line-height: 1.6;
  }

  .pub-link {
    ${({ theme }) => theme.mixins.flexCenter};
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-top: 16px;
    color: var(--green);
    font-family: var(--font-mono);
    font-size: var(--fz-xs);

    svg {
      width: 14px;
      height: 14px;
    }

    &:hover {
      text-decoration: underline;
    }
  }
`;

const publications = [
  {
    title:
      'Beyond Visualization: Building Decision Intelligence Through Iterative Dashboard Refinement',
    venue: 'arXiv, 2025',
    description:
      'First authored paper on building decision intelligence dashboards through iterative refinement. Explores how dashboards evolve from passive visualization tools to active decision support systems.',
    url: 'https://arxiv.org/abs/2510.27572',
  },
  {
    title: 'VISION: Visual Insight Solution Interface Outreach Navigator',
    venue: 'IEEE Xplore',
    description:
      'IEEE published work on an assistive computer vision wearable for the visually impaired, combining onboard sensors with real time object recognition on edge hardware.',
    url: 'https://ieeexplore.ieee.org/abstract/document/10898328',
  },
];

const Publications = () => {
  const revealContainer = useRef(null);
  const prefersReducedMotion = usePrefersReducedMotion();

  useEffect(() => {
    if (prefersReducedMotion) {
      return;
    }

    sr.reveal(revealContainer.current, srConfig());
  }, []);

  return (
    <StyledPublicationsSection id="publications" ref={revealContainer}>
      <h2 className="numbered-heading">Publications</h2>

      <StyledPublicationsList>
        {publications.map(({ title, venue, description, url }, i) => (
          <StyledPublication key={i}>
            <p className="pub-title">{title}</p>
            <p className="pub-venue">{venue}</p>
            <p className="pub-description">{description}</p>
            <a
              href={url}
              className="pub-link"
              target="_blank"
              rel="noopener noreferrer"
              aria-label={`View paper: ${title}`}>
              View Paper <Icon name="External" />
            </a>
          </StyledPublication>
        ))}
      </StyledPublicationsList>
    </StyledPublicationsSection>
  );
};

export default Publications;
